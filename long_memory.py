import json
import os

FILE = "data/long_memory.json"

# -----------------------
# ロード・セーブ
# -----------------------
def load_memory():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# -----------------------
# メモリ管理
# -----------------------
memory_state = load_memory()

def add_long_memory(user_id, text):
    """長期記憶に情報を追加"""
    if user_id not in memory_state:
        memory_state[user_id] = []

    if text not in memory_state[user_id]:
        memory_state[user_id].append(text)

    save_memory(memory_state)

def get_long_memory(user_id):
    """長期記憶を取得"""
    if user_id not in memory_state:
        return []
    return memory_state[user_id]