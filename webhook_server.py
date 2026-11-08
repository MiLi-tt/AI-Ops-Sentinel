from flask import Flask, request, jsonify, Response
import json
import threading
from ai_analyzer import analyze_logs_with_ai
from dingtalk_sender import send_dingtalk_alert
from log_parser import get_failed_logins

app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return "AI-Ops-Sentinel Webhook Server is Running!"

# 搞一个全局变量，用来保存最近一次的 AI 分析结果（给 Grafana 用）
latest_ai_analysis = {"status": "等待分析"}

@app.route('/alert', methods=['POST'])
def receive_alert():
    global latest_ai_analysis
    data = request.json
    print("\n⚠️ 收到 Prometheus 的告警请求！")
    
    try:
        alerts = data.get('alerts', [])
        if not alerts:
            return jsonify({"status": "no alerts"}), 200
            
        # 提取告警信息
        alert_info = alerts[0]
        summary = alert_info['annotations'].get('summary', '未知告警')
        description = alert_info['annotations'].get('description', '')
        
        # 提取最近的日志（结合指标+日志分析）
        print("正在拉取最近的系统安全日志...")
        recent_logs = get_failed_logins(minutes=5)
        
        # 拼装给 AI 的 Context
        combined_context = f"【指标告警】: {summary}, 详情: {description}\n"
        combined_context += f"【最近5分钟安全日志】: \n"
        for log in recent_logs:
            combined_context += log['raw'] + "\n"
            
        print("正在请求 AI 进行交叉研判...")
        # 调用 ai_analyzer
        ai_result = analyze_logs_with_ai([{"raw": combined_context}])
        
        if ai_result:
            print(f"-> AI 综合研判结果：{ai_result}")
            # 发送钉钉
            send_dingtalk_alert(ai_result)
            # 更新全局变量给 Grafana 用
            latest_ai_analysis = ai_result
            
    except Exception as e:
        print(f"处理告警时发生错误: {e}")

    return jsonify({"status": "success"}), 200

# 给 Grafana 用的接口，直接返回 HTML 代码
@app.route('/ai_status', methods=['GET'])
def get_ai_status():
    global latest_ai_analysis
    
    level = latest_ai_analysis.get('level', '等待分析')
    reason = latest_ai_analysis.get('reason', '暂无异常')
    suggestion = latest_ai_analysis.get('suggestion', '暂无建议')
    
    # 根据威胁等级改变颜色（高危/中危为红色，其他为绿色）
    color = "#d9534f" if level in ["高危", "中危"] else "#5cb85c"
    
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #111217;
                color: #d8d9da; /* 全局字体颜色改为浅灰白 */
                margin: 0;
                padding: 20px;
                font-family: 'Helvetica Neue', Arial, sans-serif;
            }}
        </style>
    </head>
    <body>
        <h2 style="color: #f0ad4e; border-bottom: 1px solid #444; padding-bottom: 10px;">🤖 最新 AI 综合研判报告</h2>

        <p style="font-size: 16px;"><strong>⚠️ 威胁等级：</strong>
            <span style="color: {color}; font-weight: bold; font-size: 20px;">{level}</span>
        </p>

        <p style="font-size: 16px; margin-top: 20px;"><strong>🔍 分析原因：</strong></p>
        <div style="background: #1f2229; padding: 15px; border-radius: 5px; border-left: 4px solid #f0ad4e; line-height: 1.6;">
            {reason}
        </div>

        <p style="font-size: 16px; margin-top: 20px;"><strong>🛠️ 修复建议：</strong></p>
        <div style="background: #1f2229; padding: 15px; border-radius: 5px; border-left: 4px solid #5cb85c; line-height: 1.6;">
            {suggestion}
        </div>
    </body>
    </html>
    """
    return Response(html_content, mimetype='text/html')

if __name__ == '__main__':
    print("🚀 Webhook 服务器启动，监听 5000 端口...")
    app.run(host='0.0.0.0', port=5000)
