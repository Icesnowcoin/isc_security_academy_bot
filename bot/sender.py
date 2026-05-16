import logging
import re
from telegram import Bot
from telegram.error import BadRequest, TelegramError
from bot.config import TARGET_CHAT_IDS
from bot.content_loader import load_topic
from bot.state_manager import get_last_index, save_last_index

logger = logging.getLogger(__name__)


def strip_markdown(text: str) -> str:
    """
    移除常见 Markdown 标记，转为纯文本。
    生产级降级策略：当 Telegram Markdown 解析失败时使用。
    """
    # 粗体 **text** → text
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text, flags=re.DOTALL)
    # 斜体 *text* → text
    text = re.sub(r'\*(.*?)\*', r'\1', text, flags=re.DOTALL)
    # 下划线 __text__ → text
    text = re.sub(r'__(.*?)__', r'\1', text, flags=re.DOTALL)
    # 行内代码 `text` → text
    text = re.sub(r'`(.*?)`', r'\1', text, flags=re.DOTALL)
    # 链接 [text](url) → text (url)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 (\2)', text, flags=re.DOTALL)
    return text


async def _send_with_fallback(bot: Bot, chat_id: int, text: str, **kwargs) -> bool:
    """
    生产级发送函数：
    1. 先尝试 Markdown 模式发送
    2. 如果因 Markdown 解析失败（400 BadRequest），自动降级到纯文本
    3. 返回是否成功送达
    """
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="Markdown",
            **kwargs
        )
        return True

    except BadRequest as e:
        error_msg = str(e).lower()
        # 判断是否为 Markdown 解析错误
        if any(k in error_msg for k in ["parse", "markdown", "entity", "can't find"]):
            logger.warning(f"[{chat_id}] Markdown 解析错误，降级到纯文本: {e}")
            try:
                plain_text = strip_markdown(text)
                await bot.send_message(
                    chat_id=chat_id,
                    text=plain_text,
                    parse_mode=None,
                    **kwargs
                )
                logger.info(f"[{chat_id}] 纯文本降级发送成功")
                return True
            except Exception as e2:
                logger.error(f"[{chat_id}] 纯文本降级也失败: {e2}")
                return False
        else:
            # 其他 BadRequest（如 chat not found, bot kicked 等）
            logger.error(f"[{chat_id}] BadRequest (非 Markdown): {e}")
            return False

    except TelegramError as e:
        logger.error(f"[{chat_id}] Telegram API 错误: {e}")
        return False
    except Exception as e:
        logger.error(f"[{chat_id}] 未知发送错误: {e}")
        return False


async def push_daily(bot: Bot, lang: str = 'zh'):
    """
    执行每日推送（生产级修复版）
    核心变更：无论发送是否成功，都推进索引，防止死循环。
    """
    idx = get_last_index()
    topic = load_topic(idx, lang)

    if not topic:
        logger.warning(f"未找到 {lang} 语言的主题内容 (index={idx})")
        # 防御性编程：内容缺失也推进索引，避免空内容导致卡死
        if lang == 'zh':
            save_last_index(idx + 1)
            logger.info(f"索引已推进 (内容缺失): {idx} -> {idx + 1}")
        return

    # 构建消息头尾
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

    # 逐群发送，带降级机制
    success_count = 0
    total_chats = len(TARGET_CHAT_IDS)
    for chat_id in TARGET_CHAT_IDS:
        if await _send_with_fallback(bot, chat_id, message, disable_web_page_preview=False):
            success_count += 1

    # 生产级关键修复：无论发送结果如何，都推进索引
    # 原因：如果因为任何错误导致 success_count=0，不推进索引会造成死循环
    # 漏掉一期比永远卡死更好，且日志会记录失败原因供排查
    if lang == 'zh':
        next_idx = idx + 1
        save_last_index(next_idx)
        logger.info(
            f"索引已推进: {idx} -> {next_idx} | "
            f"发送成功: {success_count}/{total_chats} | "
            f"主题: {topic['title']}"
        )
