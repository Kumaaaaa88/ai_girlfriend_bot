import json
import os
from datetime import datetime

FILE = "data/events.json"


def load_events():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_events(data):

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


events = load_events()


def get_events(user_id):

    if user_id not in events:
        events[user_id] = []

    return events[user_id]


def add_event(user_id, event_type, value):

    user_events = get_events(user_id)

    user_events.append({
        "type": event_type,
        "value": value,
        "date": datetime.now().strftime("%Y-%m-%d")
    })

    save_events(events)


def ensure_first_meet(user_id):

    user_events = get_events(user_id)

    for e in user_events:
        if e["type"] == "first_meet":
            return

    add_event(user_id, "first_meet", "ユナと初めて話した日")