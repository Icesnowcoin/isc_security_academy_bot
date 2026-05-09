import logging
from telegram import Bot
from bot.config import TARGET_CHAT_IDS
from bot.content_loader import load_topic
from bot.state_manager import get_last_index, save_last_index

logger = logging.getLogger(__name__)

async def push_daily(bot: Bot, lang: str = 'zh'):
    """
    执行每日推送
    :param bot: Telegram Bot 实例
    :param lang: 推送语言 ('zh' 或 'en')
    """
    idx = get_last_index()
    topic = load_topic(idx, lang)
    
    if not topic:
        logger.warning(f"未找到 {lang} 语言的主题内容")
        return

    # 根据语言定制页脚
    if lang == 'zh':
        footer = "🕐 每日12:00更新 · 社区共建 · 安全第一"
        header = "📚 *ISC 去中心化安全讲堂*"
        issue_label = "第"
        issue_suffix = "期"
    else:
        footer = "🕐 Daily 20:00 Update · Community Built · Security First"
        header = "📚 *ISC Security Academy*"
        issue_label = "Issue #"
        issue_suffix = ""

    message = (
        f"{header}\n"
        f"{issue_label} {idx + 1} {issue_suffix} | {topic['title']}\n\n"
        f"{topic['body']}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"{footer}"
    )

    success_count = 0
    for chat_id in TARGET_CHAT_IDS:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=False
            )
            logger.info(f"已推送 {lang} 内容至 {chat_id}: {topic['title']}")
            success_count += 1
        except Exception as e:
            logger.error(f"推送失败 {chat_id} ({lang}): {e}")
    
    # 只有在推送成功且为默认语言（或特定逻辑）时才增加索引
    # 这里我们设定：如果是中文推送，则增加索引（因为中文是每天第一个推送）
    if success_count > 0 and lang == 'zh':
        save_last_index(idx + 1)
