import json
import os
from datetime import datetime

from long_memory import add_long_memory
from debug import log

FILE = "data/relationship_events.json"


# -----------------------------
# load / save
# -----------------------------

def load_events():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_events(data):

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


events = load_events()


# -----------------------------
# 取得
# -----------------------------

def get_events(user_id):

    if user_id not in events:
        events[user_id] = []

    return events[user_id]


# -----------------------------
# 存在チェック
# -----------------------------

def event_exists(user_id, event_type):

    user_events = get_events(user_id)

    for e in user_events:
        if e["type"] == event_type:
            return True

    return False


# -----------------------------
# イベント追加
# -----------------------------

def add_event(user_id, event_type, description):

    if event_exists(user_id, event_type):
        return False

    user_events = get_events(user_id)

    event = {
        "type": event_type,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    user_events.append(event)

    save_events(events)

    # 思い出として長期記憶にも保存
    memory_text = f"{description} ({event['date']})"
    add_long_memory(user_id, memory_text)

    log("REL_EVENT", memory_text)

    return True


# -----------------------------
# 初会話イベント
# -----------------------------

def ensure_first_talk(user_id):

    if event_exists(user_id, "first_talk"):
        return

    add_event(
        user_id,
        "first_talk",
        "ユナと初めて会話した日"
    )


# -----------------------------
# 初ゲームイベント
# -----------------------------

GAME_WORDS = [
    "ゲーム",
    "オーバーウォッチ",
    "apex",
    "valorant",
    "lol",
]


def check_first_game(user_id, text):

    if event_exists(user_id, "first_game"):
        return

    for word in GAME_WORDS:

        if word in text:

            add_event(
                user_id,
                "first_game",
                "初めてゲームの話をした日"
            )

            return


# -----------------------------
# 長時間会話イベント
# -----------------------------

def check_long_chat(user_id, message_count):

    if message_count < 20:
        return

    if event_exists(user_id, "first_long_chat"):
        return

    add_event(
        user_id,
        "first_long_chat",
        "初めて長く話した日"
    )