# ISC 去中心化安全讲堂机器人 (ISC Security Academy Bot)

ISC（Ice Snow Coin）是一个运行在 BSC 上的完全去中心化项目。本项目是一个 Telegram 机器人，旨在每日定时向社区频道/群组推送去中心化安全教育内容。

## 项目特点
- **中英双语**：支持 22 期完整的安全教育课程，涵盖钱包安全、DEX、DeFi 基础及 ISC 项目特性。
- **定时推送**：每日北京时间 12:00 自动推送一期内容，循环播放。
- **去中心化治理**：内容强调安全防范、多签管理及社区共建。
- **自动化部署**：支持 systemd 服务管理及 GitHub Actions CI/CD。

## 目录结构
```text
.
├── bot/                  # 机器人核心代码
│   ├── main.py           # 程序入口
│   ├── config.py         # 配置管理
│   ├── sender.py         # 消息发送逻辑
│   ├── content_loader.py # 内容加载逻辑
│   └── state_manager.py  # 推送进度管理
├── content/              # 讲堂内容 (Markdown)
│   ├── zh/               # 中文版 (01-22)
│   └── en/               # 英文版 (01-22)
├── scripts/              # 部署与管理脚本
├── data/                 # 数据存储 (日志、状态)
├── .env.example          # 环境变量模板
└── requirements.txt      # 依赖列表
```

## 快速开始

### 1. 环境准备
```bash
git clone https://github.com/Icesnowcoin/isc_security_academy_bot.git
cd isc_security_academy_bot
./scripts/install.sh
```

### 2. 配置环境变量
复制 `.env.example` 为 `.env` 并填写你的机器人 Token 及目标频道 ID：
```bash
cp .env.example .env
nano .env
```

### 3. 运行机器人
```bash
./scripts/start.sh
```

## 生产环境部署 (Ubuntu)
1. 将项目放置在 `/opt/isc-security-bot`。
2. 配置 `.env` 文件。
3. 安装并启动服务：
```bash
sudo cp scripts/isc-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable isc-bot
sudo systemctl start isc-bot
```

## 课程体系 (22期)
- **模块A：钱包与交易安全** (01-06)
- **模块B：DeFi与交易所基础** (07-13)
- **模块C：ISC项目专属工具** (14-17)
- **模块D：社区共建与创业** (18-22)

## 贡献与共建
ISC 是一个去中心化项目，欢迎社区成员提交 Pull Request 完善安全讲堂内容或优化机器人代码。

---
🕐 每日12:00更新 · 社区共建 · 安全第一

