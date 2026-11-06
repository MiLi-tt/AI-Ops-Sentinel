import os
import sys
from log_parser import get_failed_logins
from ai_analyzer import analyze_logs_with_ai
from dingtalk_sender import send_dingtalk_alert

def main():
    print("=== AI-Ops-Sentinel 开始执行 ===")
    
    # 1. 提取最近 5 分钟的失败日志
    print("1. 正在扫描系统日志...")
    failed_logs = get_failed_logins(minutes=5)
    
    if not failed_logs:
        print("未发现异常日志，系统安全。退出程序。")
        sys.exit(0)
        
    print(f"   -> 发现 {len(failed_logs)} 条可疑日志，准备送入 AI 分析。")
    
    # 2. 调用 AI 进行分析
    print("2. 正在请求 AI 进行分析...")
    ai_result = analyze_logs_with_ai(failed_logs)
    
    if not ai_result:
        print("AI 分析失败，程序退出。")
        sys.exit(1)
        
    # 3. 判断是否需要告警 (高危和中危才告警)
    level = ai_result.get('level', '未知')
    print(f"   -> AI 研判结果：{level}")
    
    if level in ["高危", "中危"]:
        print("3. 触发告警条件，发送钉钉通知...")
        WEBHOOK_URL = os.getenv("DINGTALK_WEBHOOK") 
        send_dingtalk_alert(ai_result, WEBHOOK_URL)
    else:
        print("3. 威胁等级较低，本次不发送告警。")

if __name__ == "__main__":
    main()
