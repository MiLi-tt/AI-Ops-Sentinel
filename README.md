# AI-Ops Sentinel 🤖🛡️

> 一个基于大语言模型（LLM）的轻量级 Linux 智能安全告警工具。

## 📖 项目简介
传统的运维监控往往只能做到“阈值告警”，无法给出具体的故障原因。本项目基于 Python 开发，部署于 RedHat 环境，通过正则表达式实时提取系统安全日志，并调用 DeepSeek 大模型进行语义分析与威胁定级，最终通过钉钉机器人实现“告警+修复建议”的闭环推送。

## ✨ 核心特性
- **日志精准提取**：针对 `/var/log/secure` 的 SSH 暴力破解日志进行正则匹配。
- **AI 智能研判**：接入 DeepSeek API，结合运维专家 Prompt，输出结构化的 `{威胁等级, 分析原因, 修复建议}`。
- **实时告警触达**：通过钉钉 Webhook，秒级推送到手机端。
- **定时自动化**：基于 Crontab 定时执行，无需人工干预。

## 🏗️ 架构设计
<img width="1478" height="228" alt="AI-Ops Sentinel架构图" src="https://github.com/user-attachments/assets/00203fd9-c418-4cc3-8c3b-87f2cf45710c" />


## 🚀 快速开始

### 环境要求
- Linux (RedHat/CentOS)
- Python 3.8+
- DeepSeek API Key
- 钉钉机器人 Webhook

### 部署步骤
1. 克隆仓库：
   `git clone https://github.com/MiLi-tt/AI-Ops-Sentinel.git`
2. 安装依赖：
   `pip install -r requirements.txt`
3. 配置环境变量（API Key 及 Webhook）：
   `export DEEPSEEK_API_KEY="sk-xxx"`
4. 运行主程序：
   `sudo ./venv/bin/python3 main.py`

## 📸 效果展示
### 1. 终端执行
<img width="730" height="180" alt="终端告警截图" src="https://github.com/user-attachments/assets/94410601-3871-41a6-b650-0f3bd0b32e2e" />
<p align="center"><i>👆 终端展示：自动扫描系统日志、提取可疑行为并调用 AI 接口</i></p>

<br>

### 2. 钉钉机器人智能告警推送
<div align="center">
  <img width="535" height="485" alt="钉钉告警截图" src="https://github.com/user-attachments/assets/2b062997-5662-4878-bfbc-f454724d98bb" />
</div>
<p align="center"><i>👆 钉钉推送：AI 自动生成的结构化分析报告与专业修复建议</i></p>

## 🗺️ 未来规划 (Roadmap)
- [x] V1.0：实现日志提取、AI 分析与钉钉告警闭环。
- [ ] V2.0：引入 Prometheus + Grafana 监控体系，实现指标（Metrics）与日志（Logs）的融合分析。
