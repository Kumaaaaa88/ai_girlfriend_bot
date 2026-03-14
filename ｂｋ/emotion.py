# 感情システム
import json
import os

from debug import log

FILE = "data/emotion.json"


def load_data():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


emotion_state = load_data()


def get_emotion(user_id):

    if user_id not in emotion_state:
        emotion_state[user_id] = {
            "affection": 50,
            "lonely": 20,
            "jealous": 0,
            "happy": 50
        }

    return emotion_state[user_id]


def update_emotion(user_id, user_text):

    emotion = get_emotion(user_id)

    text = user_text

    if "好き" in text:
        emotion["affection"] += 5

    if "疲れ" in text:
        emotion["lonely"] += 3

    if "他の女" in text:
        emotion["jealous"] += 10

    for key in emotion:
        emotion[key] = max(0, min(100, emotion[key]))

    save_data(emotion_state)
    log("EMOTION", emotion)