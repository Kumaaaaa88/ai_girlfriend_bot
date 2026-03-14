import json

PROFILE_FILE = "data/profile.json"


def load_profiles():
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_profiles(data):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_profile(user_id):

    profiles = load_profiles()

    if user_id not in profiles:
        profiles[user_id] = {}

    return profiles[user_id]


def update_profile(user_id, key, value):

    profiles = load_profiles()

    if user_id not in profiles:
        profiles[user_id] = {}

    profiles[user_id][key] = value

    save_profiles(profiles)