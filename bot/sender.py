import logging
from telegram import Bot
from config import BOT_TOKEN, TARGET_CHAT_IDS, DEFAULT_LANG
from content_loader import load_topic, get_next_index, save_index

logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN)

async def push_daily():
    idx = get_next_index()
    for chat_id in TARGET_CHAT_IDS:
        chat_id = chat_id.strip()
        if not chat_id:
            continue
        # 可根据chat_id映射不同语言，此处默认
        topic = load_topic(idx, DEFAULT_LANG)
        if not topic:
            logger.warning("未找到主题内容")
            continue
        
        message = (
            f"📚 *ISC 去中心化安全讲堂*\n"
            f"第 {idx + 1} 期 | {topic['title']}\n\n"
            f"{topic['body']}\n\n"
            f"━━━━━━━━━━━━━━\n"
            f"🕐 每日12:00更新 · 社区共建 · 安全第一"
        )
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=False
            )
            logger.info(f"已推送至 {chat_id}: {topic['title']}")
        except Exception as e:
            logger.error(f"推送失败 {chat_id}: {e}")
    
    save_index(idx + 1)
