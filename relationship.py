import json
import os

from debug import log

FILE = "data/relationship.json"


def load_data():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


relationship_state = load_data()


def get_affection(user_id):

    if user_id not in relationship_state:
        relationship_state[user_id] = 30

    return relationship_state[user_id]


def update_affection(user_id, user_text):

    affection = get_affection(user_id)

    if "好き" in user_text:
        affection += 5

    if "ありがとう" in user_text:
        affection += 3

    if "かわいい" in user_text:
        affection += 4

    if "嫌い" in user_text:
        affection -= 10

    affection = max(0, min(100, affection))

    relationship_state[user_id] = affection

    save_data(relationship_state)
    log("AFFECTION", affection)


def get_relationship_level(affection):

    if affection < 20:
        return "初対面"

    if affection < 40:
        return "知り合い"

    if affection < 60:
        return "仲良し"

    if affection < 80:
        return "好き"

    return "恋人"
