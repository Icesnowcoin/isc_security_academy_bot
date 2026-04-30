import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_IDS = os.getenv("TARGET_CHAT_IDS", "").split(",")  # 群组/频道ID，逗号分隔
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "zh")                 # zh 或 en
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "state.json")
PUSH_HOUR = 12                                                   # 北京时间12点
PUSH_MINUTE = 0
TIMEZONE = "Asia/Shanghai"
