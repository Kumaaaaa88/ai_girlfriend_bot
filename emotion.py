import json
import time
from pathlib import Path
from debug import log

EMOTION_FILE = "data/emotion.json"

Path("data").mkdir(exist_ok=True)


# -----------------------------
# 初期データ
# -----------------------------

def default_emotion():

    return {
        "state": "normal",
        "level": 0,
        "updated_at": time.time()
    }


# -----------------------------
# load
# -----------------------------

def load_emotions():

    try:
        with open(EMOTION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


# -----------------------------
# save
# -----------------------------

def save_emotions():

    with open(EMOTION_FILE, "w", encoding="utf-8") as f:
        json.dump(emotions, f, ensure_ascii=False, indent=2)


emotions = load_emotions()


# -----------------------------
# get emotion
# -----------------------------

def get_emotion(user_id):

    user_id = str(user_id)

    if user_id not in emotions:
        emotions[user_id] = default_emotion()

    return emotions[user_id]


# -----------------------------
# update emotion
# -----------------------------

def update_emotion(user_id, text):

    user_id = str(user_id)

    emotion = get_emotion(user_id)

    happy_words = ["好き", "嬉しい", "楽しい", "ありがとう"]
    sad_words = ["疲れ", "つらい", "悲しい"]
    lonely_words = ["寂しい", "ひとり"]
    jealous_words = ["他の子", "浮気"]

    new_state = "normal"
    level = emotion["level"]

    if any(word in text for word in happy_words):
        new_state = "happy"
        level += 1

    elif any(word in text for word in sad_words):
        new_state = "sad"
        level += 1

    elif any(word in text for word in lonely_words):
        new_state = "lonely"
        level += 1

    elif any(word in text for word in jealous_words):
        new_state = "jealous"
        level += 1

    else:
        level = max(level - 1, 0)

    emotion["state"] = new_state
    emotion["level"] = min(level, 5)
    emotion["updated_at"] = time.time()

    emotions[user_id] = emotion

    save_emotions()

    log("EMOTION UPDATE", f"{user_id} → {new_state} (Lv{level})")

    return emotion


# -----------------------------
# 時間で感情を落ち着かせる
# -----------------------------

def decay_emotion(user_id):

    user_id = str(user_id)

    emotion = get_emotion(user_id)

    now = time.time()

    diff = now - emotion["updated_at"]

    # 3時間で感情レベル1減る
    hours = diff / 3600

    if hours >= 3 and emotion["level"] > 0:

        emotion["level"] -= 1
        emotion["updated_at"] = now

        if emotion["level"] == 0:
            emotion["state"] = "normal"

        emotions[user_id] = emotion

        save_emotions()

        log("EMOTION DECAY", f"{user_id} → {emotion['state']} (Lv{emotion['level']})")


# -----------------------------
# lonely連動
# -----------------------------

def apply_lonely(user_id, lonely_value):

    user_id = str(user_id)

    emotion = get_emotion(user_id)

    if lonely_value >= 3:

        emotion["state"] = "lonely"
        emotion["level"] = lonely_value

        emotions[user_id] = emotion

        save_emotions()

        log("EMOTION LONELY", f"{user_id} → lonely (Lv{lonely_value})")


# -----------------------------
# GPT用テキスト
# -----------------------------

def build_emotion_context(user_id):

    emotion = get_emotion(user_id)

    state = emotion["state"]
    level = emotion["level"]

    text = f"""
ユナの現在の感情

感情: {state}
強さ: {level}/5

感情の意味

normal → 落ち着いている
happy → 嬉しい
sad → 元気がない
lonely → 少し寂しい
jealous → 少し嫉妬

感情の強さが高いほど
その感情を会話に強く反映してください。
"""

    return text