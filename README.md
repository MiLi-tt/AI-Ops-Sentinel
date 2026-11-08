# AI-Ops Sentinel 🤖🛡️

> 一个基于大语言模型（LLM）与 Prometheus 的智能运维（AIOps）监控与安全告警闭环系统。

## 📖 项目简介

传统的运维监控往往只能做到“阈值告警”（例如：CPU > 80%），无法结合系统上下文给出具体的故障原因；而单纯分析系统日志又缺乏指标数据的支撑。

本项目基于 Python 开发，部署于 RedHat 环境。**V1.0** 实现了基于日志的智能安全研判；**V2.0** 完成了架构演进，接入了 `Prometheus + Alertmanager + Grafana` 体系。当系统指标（如 CPU 飙升）触发告警时，Python 服务会主动拉取当前系统的安全日志，将**“指标告警”与“安全日志”进行交叉验证**，并调用 DeepSeek 大模型进行根因分析。最终将分析报告通过钉钉机器人实时推送，并展示在 Grafana 监控大屏上。

## ✨ 核心特性

- **全栈监控体系**：Node Exporter 采集指标，Prometheus 存储与告警，Grafana 可视化展示。
- **指标与日志交叉分析 (RCA)**：结合硬件指标（Metrics）和安全日志（Logs）作为 Context 喂给大模型，实现精准的根因定位。
- **AI 智能研判**：接入 DeepSeek 大模型，结合运维专家 Prompt，输出结构化的 `{威胁等级, 分析原因, 修复建议}`。
- **双通道告警闭环**：通过钉钉 Webhook 推送到手机，并同步在 Grafana 呈现高颜值的诊断面板。
- **工程化规范**：敏感信息（API Key/Webhook）环境变量隔离，Crontab 定时调度，Git 规范提交。

## 🏗️ 架构设计
<img width="6088" height="1576" alt="AI-Ops Sentinel架构图2 0" src="https://github.com/user-attachments/assets/f596efce-9ef3-4322-8cdc-6458edd93a00" />

## 🚀 快速开始

### 环境要求
- Linux (RedHat/CentOS)
- Python 3.8+
- Prometheus 生态组件 (Node Exporter, Alertmanager, Grafana)
- DeepSeek API Key
- 钉钉机器人 Webhook

### 部署步骤
1. 克隆仓库：
   `git clone https://github.com/MiLi-tt/AI-Ops-Sentinel.git`
2. 安装依赖：
   `pip install -r requirements.txt`
3. 配置环境变量（API Key 及 Webhook，禁止硬编码在代码中）：
   `export DEEPSEEK_API_KEY="sk-xxx"`
   `export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=xxx"`
4. 启动 Flask Webhook 接收服务：
   `nohup ./venv/bin/python3 webhook_server.py >> webhook.log 2>&1 &`
5. 配置 Prometheus 与 Alertmanager：
   将仓库 `configs/` 目录下的配置文件分别复制到对应的安装目录，并重启服务。
6. 启动定时任务（V1.0 模块）：
   `sudo crontab -e` (添加 `*/5 * * * * /root/AI-Ops-Sentinel/venv/bin/python3 /root/AI-Ops-Sentinel/main.py ...`)

## 📸 效果展示

### 1. 终端执行与告警触发
<div align="center">
   <img width="730" height="180" alt="终端告警截图" src="https://github.com/user-attachments/assets/94410601-3871-41a6-b650-0f3bd0b32e2e" />
</div>
<p align="center"><i>👆 终端展示：自动扫描系统日志、提取可疑行为并调用 AI 接口</i></p>

<br>

### 2. 钉钉机器人智能告警推送
<div align="center">
  <img width="720" height="574" alt="钉钉告警截图" src="https://github.com/user-attachments/assets/68b1d171-acbd-4c08-b5e7-a18366f236be" />
</div>
<p align="center"><i>👆 钉钉推送：AI 自动生成的结构化分析报告与专业修复建议</i></p>

<br>

### 3. Grafana AIOps 综合监控大屏 (V2.0 新增)
<img width="1910" height="1035" alt="面板截图" src="https://github.com/user-attachments/assets/cb03ebc9-0f4e-4916-a568-732f2a5a8041" />
<p align="center"><i>👆 Grafana 大屏：实时监控指标，并在右侧无缝嵌入 AI 交叉研判报告</i></p>

## 🗺️ 踩坑与演进记录 (Roadmap)
- [x] **V1.0**：实现日志提取、AI 分析与钉钉告警闭环。
- [x] **V2.0**：引入 Prometheus + Grafana 监控体系，实现指标（Metrics）与日志（Logs）的融合分析。解决 Crontab 环境变量丢失、Grafana JSON 插件变量不渲染等痛点。
- [ ] **V3.0 (规划中)**：引入 Docker Compose 一键部署；使用 Ansible 实现自动化下发；尝试接入本地私有化大模型保障数据安全。
