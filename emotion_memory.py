import json
import os
import random
from datetime import datetime

from debug import log
from long_memory import add_long_memory

FILE = "data/emotion_memory.json"


# -----------------------------
# load / save
# -----------------------------

def load_data():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


data = load_data()


# -----------------------------
# memory追加
# -----------------------------

def add_emotion_memory(user_id, text, emotion, importance=0.5):

    if user_id not in data:
        data[user_id] = []

    memory = {

        "text": text,
        "emotion": emotion,
        "importance": importance,
        "date": datetime.now().strftime("%Y-%m-%d")

    }

    data[user_id].append(memory)

    save_data(data)

    # 長期記憶にも保存
    add_long_memory(user_id, text)

    log("EMOTION_MEMORY", text)


# -----------------------------
# 取得
# -----------------------------

def get_emotion_memories(user_id):

    if user_id not in data:
        return []

    return data[user_id]


# -----------------------------
# 感情に合う記憶取得
# -----------------------------

def get_memories_by_emotion(user_id, emotion):

    memories = get_emotion_memories(user_id)

    result = []

    for m in memories:

        if m["emotion"] == emotion:
            result.append(m)

    return result


# -----------------------------
# ランダム思い出
# -----------------------------

def get_random_memory(user_id):

    memories = get_emotion_memories(user_id)

    if not memories:
        return None

    return random.choice(memories)