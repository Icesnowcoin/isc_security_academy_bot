import os
import glob
from config import CONTENT_DIR, DEFAULT_LANG

def load_topic(index: int, lang: str = DEFAULT_LANG):
    """按索引加载指定语言的主题内容"""
    pattern = os.path.join(CONTENT_DIR, lang, "*.md")
    # 确保按文件名排序，如 01_xxx.md, 02_xxx.md
    files = sorted(glob.glob(pattern))
    if not files:
        return None
    
    # 循环播放：如果索引超过文件总数，则取模
    idx = index % len(files)
    filepath = files[idx]
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if not lines:
            return None
            
        title = lines[0].replace("#", "").strip()
        body = "".join(lines[1:]).strip()
        return {"index": idx, "title": title, "body": body, "source": filepath}
    except Exception:
        return None
