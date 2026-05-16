import asyncio
import sys
import os

# 确保脚本能找到 bot 目录下的模块
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "bot"))

from sender import push_daily

async def main():
    print("--- ISC Bot 手动推送工具 ---")
    print("正在尝试触发推送任务...")
    await push_daily()
    print("任务执行完毕，请检查 Telegram 频道。")

if __name__ == "__main__":
    asyncio.run(main())
