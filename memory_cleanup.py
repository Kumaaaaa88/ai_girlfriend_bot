import os
import json
import time

from memory_importance import calculate_importance

DATA_DIR = "data"

LONG_MEMORY_FILE = os.path.join(DATA_DIR, "long_memory.json")
VECTOR_MEMORY_FILE = os.path.join(DATA_DIR, "vector_memory.json")


# -----------------------------
# JSONロード
# -----------------------------

def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# JSON保存
# -----------------------------

def save_json(path, data):

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -----------------------------
# Long Memory Cleanup
# -----------------------------

def cleanup_long_memory(max_memories=50):

    data = load_json(LONG_MEMORY_FILE)

    for user_id in data:

        memories = data[user_id]

        scored = []

        for m in memories:

            score = calculate_importance(m)

            scored.append((score, m))

        # 重要度順
        scored.sort(reverse=True)

        # 上位だけ残す
        data[user_id] = [m for score, m in scored[:max_memories]]

    save_json(LONG_MEMORY_FILE, data)


# -----------------------------
# Vector Memory Cleanup
# -----------------------------

def cleanup_vector_memory(max_memories=200):

    data = load_json(VECTOR_MEMORY_FILE)

    # userごと整理
    user_map = {}

    for item in data:

        user_id = item["user_id"]

        user_map.setdefault(user_id, []).append(item)

    cleaned = []

    for user_id, items in user_map.items():

        # importance
        scored = []

        for item in items:

            text = item["text"]

            score = calculate_importance(text)

            scored.append((score, item))

        scored.sort(reverse=True)

        cleaned.extend([item for score, item in scored[:max_memories]])

    save_json(VECTOR_MEMORY_FILE, cleaned)


# -----------------------------
# 全cleanup
# -----------------------------

def run_memory_cleanup():

    print("Memory cleanup start")

    cleanup_long_memory()
    cleanup_vector_memory()

    print("Memory cleanup complete")