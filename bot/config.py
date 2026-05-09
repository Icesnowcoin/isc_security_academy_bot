import os
from dotenv import load_dotenv

# 加载项目根目录下的 .env 文件
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# 基础配置
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_IDS = [cid.strip() for cid in os.getenv("TARGET_CHAT_IDS", "").split(",") if cid.strip()]
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "zh")

# 路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
DATA_DIR = os.path.join(BASE_DIR, "data")
STATE_FILE = os.path.join(DATA_DIR, "state.json")

# 推送时间配置 (24小时制)
PUSH_HOUR_ZH = int(os.getenv("PUSH_HOUR_ZH", "12"))
PUSH_MINUTE_ZH = int(os.getenv("PUSH_MINUTE_ZH", "0"))
PUSH_HOUR_EN = int(os.getenv("PUSH_HOUR_EN", "20"))
PUSH_MINUTE_EN = int(os.getenv("PUSH_MINUTE_EN", "0"))
TIMEZONE = os.getenv("TIMEZONE", "Asia/Shanghai")

# 合约与链接配置
ISC_CONTRACT = os.getenv("ISC_CONTRACT", "0x11229a3f976566FA8a3ba462C432122f3B8876f6")
ISC_SYMBOL = os.getenv("ISC_SYMBOL", "ISC")
DEXSCREENER_API = os.getenv("DEXSCREENER_API", "https://api.dexscreener.com/latest/dex/tokens/")
PANCAKESWAP_URL = os.getenv("PANCAKESWAP_URL", "https://pancakeswap.finance/swap?outputCurrency=" + ISC_CONTRACT)
BSCSCAN_URL = os.getenv("BSCSCAN_URL", "https://bscscan.com/token/" + ISC_CONTRACT)
WEBSITE = os.getenv("WEBSITE", "https://icesnowcoin.com")
WHITEPAPER = os.getenv("WHITEPAPER", "https://icesnowcoin.org/whitepaper")
X_TWITTER = os.getenv("X_TWITTER", "https://x.com/icesnowcoin")
TELEGRAM_GROUP = os.getenv("TELEGRAM_GROUP", "https://t.me/ISC_Official")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT", "https://t.me/ISC_Security_Academy")
GITHUB = os.getenv("GITHUB", "https://github.com/Icesnowcoin")
AUDIT_REPORT = os.getenv("AUDIT_REPORT", "https://icesnowcoin.org/audit")
