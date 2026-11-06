import os
import json
import requests

def analyze_logs_with_ai(logs):
    """
    将日志发送给大模型，获取结构化的分析结果
    """
    # 从环境变量读取 API Key
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：未找到 DEEPSEEK_API_KEY 环境变量，请先配置。")
        return None

    # 如果日志为空，直接返回
    if not logs:
        return {"level": "安全", "reason": "无异常日志", "suggestion": "无需处理"}

    # 把字典列表转换成纯文本格式，方便发给 AI
    log_text = "\n".join([log['raw'] for log in logs])

    # 构造 Prompt（提示词），这是 AIOps 的核心！
    system_prompt = """
    你是一个资深的 Linux 运维专家和安全专家。
    你的任务是分析用户提供的系统日志，判断是否存在安全威胁或系统故障。
    请务必以严格的 JSON 格式输出，不要包含任何 Markdown 标记（如 ```json ），JSON 结构如下：
    {
        "level": "高危/中危/低危/安全",
        "reason": "分析得出此结论的原因",
        "suggestion": "给运维工程师的具体修复或排查建议"
    }
    """

    user_prompt = f"请分析以下 RedHat 系统的安全日志片段：\n{log_text}"

    # DeepSeek 的 API 接口地址
    url = "https://api.deepseek.com/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "deepseek-chat", # 使用 DeepSeek 对话模型
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1 # 温度越低，输出越稳定严谨，适合运维场景
    }

    try:
        print("正在呼叫 AI 专家进行分析...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status() # 如果 HTTP 状态码不是 200，抛出异常
        
        # 解析返回的 JSON
        result = response.json()
        ai_content = result['choices'][0]['message']['content']
        
        # 因为 AI 可能会在 JSON 前后加废话，我们提取出真正的 JSON
        # 寻找第一个 { 和最后一个 } 之间的内容
        start_idx = ai_content.find('{')
        end_idx = ai_content.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            json_str = ai_content[start_idx:end_idx]
            return json.loads(json_str)
        else:
            print(f"AI 返回格式异常：{ai_content}")
            return None

    except Exception as e:
        print(f"调用 AI 接口失败: {e}")
        return None

# 写一段测试代码，当直接运行此文件时触发
if __name__ == "__main__":
    # 伪造一条日志用于测试
    mock_logs = [
        {"time": "Oct 26 10:15:00", "ip": "192.168.1.100", "raw": "Oct 26 10:15:00 sentinel sshd[1234]: Failed password for root from 192.168.1.100 port 12345 ssh2"}
    ]
    
    print("--- 测试 AI 分析功能 ---")
    result = analyze_logs_with_ai(mock_logs)
    if result:
        print("\n✅ AI 分析结果：")
        print(f"威胁等级：{result.get('level')}")
        print(f"分析原因：{result.get('reason')}")
        print(f"修复建议：{result.get('suggestion')}")
