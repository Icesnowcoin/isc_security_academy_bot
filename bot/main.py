import asyncio
import logging
import os
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# 确保日志目录存在
log_path = '/opt/isc-security-bot/data/logs/bot.log'
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# 日志同时写入文件 + stdout（systemd journal 可见）
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def safe_push(lang='zh'):
    """
    安全推送包装器：
    每次推送独立捕获异常，避免单次失败影响调度器。
    如果 sender 使用异步 Telegram 库，在此函数内完成调用。
    """
    try:
        # 动态导入，避免启动时循环依赖
        from bot import sender
        
        # 兼容可能的函数名：push_daily / send_daily / run_push_daily
        if hasattr(sender, 'push_daily'):
            await sender.push_daily(lang=lang)
        elif hasattr(sender, 'send_daily'):
            await sender.send_daily(lang=lang)
        elif hasattr(sender, 'run_push_daily'):
            await sender.run_push_daily()
        else:
            logger.error("sender 模块没有可识别的推送函数")
            return
            
        logger.info(f"✅ 已推送 {lang} 内容至频道")
    except Exception as e:
        logger.error(f"❌ 推送失败: {e}", exc_info=True)

def start_scheduler():
    """启动双推定时器：北京时间 12:00 中文 + 20:00 英文"""
    tz = 'Asia/Shanghai'
    scheduler = AsyncIOScheduler(timezone=tz)
    
    # 中文推送
    scheduler.add_job(
        safe_push,
        CronTrigger(hour=12, minute=0),
        args=['zh'],
        id='push_zh',
        replace_existing=True
    )
    
    # 英文推送
    scheduler.add_job(
        safe_push,
        CronTrigger(hour=20, minute=0),
        args=['en'],
        id='push_en',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("🚀 定时任务已启动：北京时间 12:00(中文) 和 20:00(英文)")

async def main():
    start_scheduler()
    # 根治 Event loop is closed：使用 Event 等待，替代 run_forever()
    stop_event = asyncio.Event()
    await stop_event.wait()

if __name__ == '__main__':
    asyncio.run(main())
