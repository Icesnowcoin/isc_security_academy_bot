import asyncio, signal, sys
from scheduler import start_scheduler

def shutdown(signum, frame):
    print("收到终止信号，正在退出...")
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

if __name__ == "__main__":
    scheduler = start_scheduler()
    print("ISC安全讲堂机器人运行中...")
    # 保持主线程存活
    asyncio.get_event_loop().run_forever()
