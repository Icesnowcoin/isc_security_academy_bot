import logging
from telegram import Bot
from telegram.constants import ParseMode
from config import BOT_TOKEN, TARGET_CHAT_IDS, DEFAULT_LANG
from content_loader import load_topic
from state_manager import get_last_index, save_last_index

logger = logging.getLogger(__name__)
bot = Bot(token=BOT_TOKEN)

async def push_daily():
    idx = get_last_index()
    topic = load_topic(idx, DEFAULT_LANG)
    
    if not topic:
        logger.warning(f"未找到主题内容 (Index: {idx})")
        return

    title = topic['title']
    body = topic['body']
    
    # 构造标准消息
    message = (
        f"📚 *ISC 去中心化安全讲堂*\n"
        f"第 {idx + 1} 期 | {title}\n\n"
        f"{body}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"🕐 每日12:00更新 · 社区共建 · 安全第一"
    )

    success_count = 0
    for chat_id in TARGET_CHAT_IDS:
        chat_id = chat_id.strip()
        if not chat_id: continue
        
        try:
            # 优先尝试 Markdown 模式
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False
            )
            logger.info(f"已推送至 {chat_id}: {title}")
            success_count += 1
        except Exception as e:
            logger.error(f"Markdown 推送失败，尝试纯文本补发: {e}")
            try:
                # 容错：如果 Markdown 报错，移除标记符以纯文本发送
                await bot.send_message(
                    chat_id=chat_id,
                    text=message.replace("*", "").replace("_", ""),
                    disable_web_page_preview=False
                )
                logger.info(f"已通过纯文本模式补发至 {chat_id}")
                success_count += 1
            except Exception as e2:
                logger.error(f"纯文本补发也失败: {e2}")
    
    # 只要有一个成功发送，就推进到下一期
    if success_count > 0:
        save_last_index(idx + 1)
