from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from config import PUSH_HOUR, PUSH_MINUTE, TIMEZONE
from sender import push_daily
import logging
import asyncio

logger = logging.getLogger(__name__)

def job_wrapper():
    """桥接异步函数到定时器线程"""
    logger.info("触发定时推送任务...")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(push_daily())
        loop.close()
    except Exception as e:
        logger.error(f"定时任务执行失败: {e}")

def start_scheduler():
    tz = timezone(TIMEZONE)
    scheduler = BackgroundScheduler(timezone=tz)
    scheduler.add_job(
        job_wrapper,
        trigger=CronTrigger(hour=PUSH_HOUR, minute=PUSH_MINUTE),
        id="daily_security_lecture",
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"定时器已启动，每日 {PUSH_HOUR:02d}:{PUSH_MINUTE:02d} 推送")
    return scheduler
