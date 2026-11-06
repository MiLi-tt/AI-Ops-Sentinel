import re
import time
from datetime import datetime, timedelta

def get_failed_logins(log_file="/var/log/secure", minutes=5):
    """
    读取 /var/log/secure 文件，提取过去 {minutes} 分钟内 SSH 登录失败的日志。
    """
    failed_logs = []
    # 获取当前时间和 {minutes} 分钟前的时间
    now = datetime.now()
    time_threshold = now - timedelta(minutes=minutes)
    
    # 定义匹配 SSH 登录失败的正则表达式
    # 匹配格式类似于：Oct 26 10:15:00 sentinel sshd[1234]: Failed password for root from 192.168.1.100 port 12345 ssh2
    pattern = re.compile(r'Failed password for .* from (\d+\.\d+\.\d+\.\d+)')

    try:
        with open(log_file, 'r') as f:
            # 日志通常很大，为了简单起见，V1.0 先读取最后 1000 行
            lines = f.readlines()[-1000:]
            
            for line in lines:
                # 简单的时间过滤（这里用字符串截取匹配，真实生产建议用正则解析时间）
                # 假设日志开头格式为 "Oct 26 10:15:00"
                try:
                    log_time_str = line[:15]
                    # 将日志时间转换为 datetime 对象，加上当前年份
                    log_time = datetime.strptime(f"{now.year} {log_time_str}", "%Y %b %d %H:%M:%S")
                    
                    if log_time >= time_threshold:
                        # 如果时间在阈值内，再匹配 "Failed password"
                        match = pattern.search(line)
                        if match:
                            ip = match.group(1)
                            failed_logs.append({"time": log_time_str, "ip": ip, "raw": line.strip()})
                except ValueError:
                    # 遇到无法解析时间的行（比如跨年日志或格式不对），直接跳过
                    continue
                    
    except FileNotFoundError:
        print(f"错误：找不到日志文件 {log_file}")
    except PermissionError:
        print(f"错误：没有权限读取 {log_file}，请使用 sudo 运行此脚本。")
        
    return failed_logs

if __name__ == "__main__":
    print("正在扫描最近的 SSH 登录失败日志...")
    logs = get_failed_logins(minutes=10) # 测试时我们放宽到最近 10 分钟
    
    if logs:
        print(f"发现 {len(logs)} 条可疑登录失败记录：")
        for log in logs:
            print(f"时间: {log['time']}, 攻击源 IP: {log['ip']}")
    else:
        print("最近 10 分钟内未发现 SSH 登录失败记录。系统安全。")
