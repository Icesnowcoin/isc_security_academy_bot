from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from config import PUSH_HOUR, PUSH_MINUTE, TIMEZONE
from sender import push_daily
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_scheduler():
    tz = timezone(TIMEZONE)
    scheduler = BackgroundScheduler(timezone=tz)
    scheduler.add_job(
        push_daily,
        trigger=CronTrigger(hour=PUSH_HOUR, minute=PUSH_MINUTE),
        id="daily_security_lecture",
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"定时任务已启动：北京时间 {PUSH_HOUR:02d}:{PUSH_MINUTE:02d}")
    return scheduler
