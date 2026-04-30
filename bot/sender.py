import logging
from telegram import Bot
from config import BOT_TOKEN, TARGET_CHAT_IDS, DEFAULT_LANG
from content_loader import load_topic
from state_manager import get_last_index, save_last_index

logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN)

async def push_daily():
    idx = get_last_index()
    topic = load_topic(idx, DEFAULT_LANG)
    
    if not topic:
        logger.warning("未找到主题内容")
        return

    message = (
        f"📚 *ISC 去中心化安全讲堂*\n"
        f"第 {idx + 1} 期 | {topic['title']}\n\n"
        f"{topic['body']}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕐 每日12:00更新 · 社区共建 · 安全第一"
    )

    success_count = 0
    for chat_id in TARGET_CHAT_IDS:
        chat_id = chat_id.strip()
        if not chat_id:
            continue
        
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=False
            )
            logger.info(f"已推送至 {chat_id}: {topic['title']}")
            success_count += 1
        except Exception as e:
            logger.error(f"推送失败 {chat_id}: {e}")
    
    if success_count > 0:
        save_last_index(idx + 1)
