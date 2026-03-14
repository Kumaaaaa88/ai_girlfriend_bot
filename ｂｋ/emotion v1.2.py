import json
from debug import log

EMOTION_FILE = "data/emotion.json"


def load_emotion():
    try:
        with open(EMOTION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_emotion():
    with open(EMOTION_FILE, "w", encoding="utf-8") as f:
        json.dump(emotions, f, ensure_ascii=False, indent=2)


emotions = load_emotion()


def get_emotion(user_id):

    user_id = str(user_id)

    if user_id not in emotions:
        emotions[user_id] = "normal"

    return emotions[user_id]


def update_emotion(user_id, text):

    user_id = str(user_id)

    emotion = get_emotion(user_id)

    happy_words = ["好き", "嬉しい", "楽しい", "ありがとう"]
    sad_words = ["疲れ", "つらい", "悲しい"]
    lonely_words = ["寂しい", "ひとり"]

    if any(word in text for word in happy_words):
        emotion = "happy"

    elif any(word in text for word in sad_words):
        emotion = "sad"

    elif any(word in text for word in lonely_words):
        emotion = "lonely"

    else:
        emotion = "normal"

    emotions[user_id] = emotion
    save_emotion()

    log("EMOTION UPDATE", f"{user_id} → {emotion}")