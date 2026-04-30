import os, json, glob
from config import CONTENT_DIR, STATE_FILE, DEFAULT_LANG

def load_topic(index: int, lang: str = DEFAULT_LANG):
    """按索引加载指定语言的主题内容"""
    pattern = os.path.join(CONTENT_DIR, lang, "*.md")
    files = sorted(glob.glob(pattern))
    if not files:
        return None
    idx = index % len(files)
    filepath = files[idx]
    
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    title = lines[0].replace("# ", "").strip() if lines else "Untitled"
    body = "".join(lines[1:]).strip()
    return {"index": idx, "title": title, "body": body, "source": filepath}

def get_next_index():
    """读取状态文件，返回下一个应推送的索引"""
    if not os.path.exists(STATE_FILE):
        return 0
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        state = json.load(f)
    return state.get("last_index", 0)

def save_index(index: int):
    """保存推送进度"""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"last_index": index}, f, ensure_ascii=False)
