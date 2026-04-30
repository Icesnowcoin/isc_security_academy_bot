import os
import json
from config import STATE_FILE

def get_last_index():
    """读取状态文件，返回上一次推送的索引"""
    if not os.path.exists(STATE_FILE):
        return 0
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state.get("last_index", 0)
    except (json.JSONDecodeError, IOError):
        return 0

def save_last_index(index: int):
    """保存推送进度"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_index": index}, f, ensure_ascii=False)
