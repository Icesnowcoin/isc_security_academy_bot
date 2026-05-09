import os
import logging
import asyncio
from datetime import datetime, time
import pytz
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    ChatMemberHandler, 
    ContextTypes, 
    filters, 
    JobQueue
)
from telegram.constants import ParseMode, ChatMemberStatus
from dotenv import load_dotenv

# 统一导入路径
from bot.sender import push_daily as security_push_daily
from bot.config import (
    BOT_TOKEN, PUSH_HOUR_ZH, PUSH_MINUTE_ZH, PUSH_HOUR_EN, PUSH_MINUTE_EN, 
    TIMEZONE, TARGET_CHAT_IDS, ISC_CONTRACT, WEBSITE, WHITEPAPER, 
    PANCAKESWAP_URL, BSCSCAN_URL, X_TWITTER, TELEGRAM_GROUP, 
    TELEGRAM_CHAT, GITHUB, AUDIT_REPORT, DEXSCREENER_API
)

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 防骗关键词
SCAM_KEYWORDS = ["私钥", "private key", "助记词", "seed phrase", "seed", "转账给我", "send me", "打钱", "给我转", "充值", "investment plan", "guaranteed return", "翻倍", "保本"]

# ==================== 辅助函数 ====================
async def fetch_price():
    """获取 ISC 实时价格"""
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{DEXSCREENER_API}{ISC_CONTRACT}"
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    pairs = data.get("pairs", [])
                    if pairs:
                        pair = pairs[0]
                        return {
                            "price": pair.get("priceUsd", "N/A"),
                            "change24h": pair.get("priceChange", {}).get("h24", "N/A"),
                            "liquidity": pair.get("liquidity", {}).get("usd", "0"),
                            "fdv": pair.get("fdv", "0"),
                        }
    except Exception as e:
        logger.error(f"价格获取失败: {e}")
    return None

# ==================== 命令处理器 ====================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "❄️ *欢迎来到 Ice Snow Coin (ISC) 社区！*\n\n"
        "你好，我是 ISC 社区助手 Bot。\n\n"
        "🔹 *关于 ISC*\n"
        "AI 驱动的 GameFi + NFT 生态系统，连接虚拟与现实世界。\n\n"
        "📌 *常用命令*\n"
        "/price - 查询实时价格\n"
        "/contract - 合约详情与链接\n"
        "/security - 安全与审计信息\n"
        "/links - 官方链接汇总\n\n"
        "⚠️ *风险提示*\n"
        "加密货币投资具有高风险，请自行进行尽职调查。"
    )
    keyboard = [
        [InlineKeyboardButton("🌐 官网", url=WEBSITE), InlineKeyboardButton("📄 白皮书", url=WHITEPAPER)],
        [InlineKeyboardButton("🔄 PancakeSwap 交易", url=PANCAKESWAP_URL)],
        [InlineKeyboardButton("🔍 BSCScan", url=BSCSCAN_URL)]
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN)

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = await fetch_price()
    if data:
        msg = (
            f"📊 *ISC 实时行情*\n\n"
            f"💰 价格: `${data['price']}`\n"
            f"📈 24h 涨跌: `{data['change24h']}%`\n"
            f"💧 流动性: `${float(data['liquidity']):,.2f}`\n"
            f"市值: `${float(data['fdv']):,.0f}`"
        )
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("❌ 暂时无法获取价格，请稍后再试。")

async def security_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = (
        "🛡️ *ISC 安全与审计*\n\n"
        "• *审计*: TechRate (全部通过)\n"
        "• *所有权*: 已永久放弃\n"
        "• *流动性*: 40% LP 已在 UNCX 锁定\n"
        "• *团队代币*: 20% 已在 Team Finance 锁定\n\n"
        f"[查看审计报告]({AUDIT_REPORT})"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = (
        "🔗 *ISC 官方链接*\n\n"
        f"• [官网]({WEBSITE})\n"
        f"• [X (Twitter)]({X_TWITTER})\n"
        f"• [Telegram 群组]({TELEGRAM_GROUP})\n"
        f"• [Telegram 频道]({TELEGRAM_CHAT})\n"
        f"• [GitHub]({GITHUB})"
    )
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = "📖 *帮助指南*\n\n使用以下命令与我交互：\n/price - 实时价格\n/contract - 合约信息\n/security - 安全审计\n/links - 官方链接"
    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

# ==================== 消息处理 ====================
async def handle_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理新成员加入"""
    result = update.chat_member
    if result.old_chat_member.status == ChatMemberStatus.LEFT and result.new_chat_member.status == ChatMemberStatus.MEMBER:
        user_name = result.new_chat_member.user.full_name
        welcome_msg = f"🎉 欢迎 {user_name} 加入 ISC 社区！输入 /start 了解更多。"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_msg)

async def anti_scam_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """反诈骗检测"""
    if not update.message or not update.message.text: return
    text = update.message.text.lower()
    if any(kw in text for kw in SCAM_KEYWORDS):
        await update.message.reply_text("⚠️ *安全提醒*：请勿分享私钥或助记词！谨防诈骗！", parse_mode=ParseMode.MARKDOWN)

# ==================== 定时任务 ====================
async def scheduled_push_zh(context: ContextTypes.DEFAULT_TYPE):
    await security_push_daily(context.bot, lang='zh')

async def scheduled_push_en(context: ContextTypes.DEFAULT_TYPE):
    await security_push_daily(context.bot, lang='en')

# ==================== 主循环 (P0 修复) ====================
async def main() -> None:
    # 1. 初始化 Application
    application = Application.builder().token(BOT_TOKEN).build()

    # 2. 注册处理器
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("price", price_command))
    application.add_handler(CommandHandler("security", security_command))
    application.add_handler(CommandHandler("links", links_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(ChatMemberHandler(handle_chat_member, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_scam_handler))

    # 3. 配置定时任务
    tz = pytz.timezone(TIMEZONE)
    application.job_queue.run_daily(scheduled_push_zh, time=time(hour=PUSH_HOUR_ZH, minute=PUSH_MINUTE_ZH, tzinfo=tz))
    application.job_queue.run_daily(scheduled_push_en, time=time(hour=PUSH_HOUR_EN, minute=PUSH_MINUTE_EN, tzinfo=tz))

    # 4. 手动生命周期管理 (解决 P0 事件循环冲突)
    await application.initialize()
    await application.start()
    
    # 显式启动 JobQueue (在 initialize 之后)
    if application.job_queue:
        await application.job_queue.start()
        
    logger.info("ISC Master Bot 已通过手动生命周期管理启动 (PTB 20.7)")
    
    # 启动轮询
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    
    # 保持运行直至接收到信号
    stop_event = asyncio.Event()
    
    # 可以在这里添加信号处理逻辑，但 asyncio.Event().wait() 是最稳健的挂起方式
    try:
        await stop_event.wait()
    except (KeyboardInterrupt, SystemExit):
        logger.info("正在关闭机器人...")
    finally:
        if application.updater:
            await application.updater.stop()
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
