import json
import os

from debug import log

FILE = "data/memory.json"


def load_memory():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(data):

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


memory = load_memory()


def add_message(user_id, role, content):

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({
        "role": role,
        "content": content
    })

    memory[user_id] = memory[user_id][-10:]

    save_memory(memory)
    log("MEMORY SAVED", user_id)

def get_memory(user_id):

    if user_id not in memory:
        return []

    return memory[user_id]