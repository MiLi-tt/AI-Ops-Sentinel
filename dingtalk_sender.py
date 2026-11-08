import os
import requests
import json

def send_dingtalk_alert(ai_result, webhook_url=None):
    """
    将 AI 的分析结果发送到钉钉群
    """
    if not ai_result:
        return

    if not webhook_url:
        webhook_url = os.getenv("DINGTALK_WEBHOOK")
        
    if not webhook_url:
        print("❌ 错误：未找到 DINGTALK_WEBHOOK 环境变量，请检查配置。")
        return

    # 组装 Markdown 格式的消息
    markdown_text = f"""
### ⚠️ 系统安全告警

**🔴 威胁等级**：{ai_result.get('level', '未知')}

**🔍 分析原因**：
{ai_result.get('reason', '无')}

**🛠️ 修复建议**：
{ai_result.get('suggestion', '无')}

---
*本消息由 AI-Ops-Sentinel 自动生成*
"""

    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "AI 运维告警",
            "text": markdown_text
        }
    }

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data), timeout=10)
        response.raise_for_status()
        res_json = response.json()
        if res_json.get("errcode") == 0:
            print("✅ 钉钉告警发送成功！请查看手机。")
        else:
            print(f"❌ 钉钉发送被拦截，错误信息: {res_json}")
            
    except Exception as e:
        print(f"❌ 钉钉告警发送失败: {e}")

if __name__ == "__main__":
    # 测试发送
    test_result = {
        "level": "高危",
        "reason": "测试：检测到针对 root 用户的 SSH 暴力破解。",
        "suggestion": "请立即封禁该 IP。"
    }
    send_dingtalk_alert(test_result)
