import json
import time
import os

from datetime import datetime, timedelta
from typing import Any

DATA_FILE = "data/activity.json"

activity_state = {}


class ActivityTracker:

    def __init__(self):

        if not os.path.exists(DATA_FILE):

            data = {
                "last_user_message": 0,
                "last_user_id": None,
                "last_channel_id": None,
                "lonely": 0
            }

            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)

    def load(self):

        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def save(self, data):

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    # -------------------------
    # ユーザー発言更新
    # -------------------------

    def update_user_activity(self, user_id, channel_id):

        data = self.load()

        data["last_user_message"] = time.time()
        data["last_user_id"] = user_id
        data["last_channel_id"] = channel_id
        data["lonely"] = 0 # ユーザーが会話したため寂しさをリセット

        self.save(data)

    # -------------------------
    # 最後の会話時間
    # -------------------------

    def hours_since_last_message(self):

        data = self.load()

        last = data["last_user_message"]

        if last == 0:
            return 999

        return (time.time() - last) / 3600

    # -------------------------
    # 寂しさ取得
    # -------------------------

    def get_lonely(self):

        data = self.load()

        return data["lonely"]

    # -------------------------
    # 寂しさ更新
    # -------------------------

    def update_lonely(self):

        data = self.load()

        hours = self.hours_since_last_message()
        # 時間経過で寂しさを更新　１時間で１
        lonely = int(hours)

        data["lonely"] = lonely

        self.save(data)

        return lonely

    # -------------------------
    # 自発会話判定
    # -------------------------

    def should_start_conversation(self, affection=50):

        lonely = self.update_lonely()

        if lonely == 0:
            return False
        # 最後の会話から１時間経つ場合自発会話
        if lonely >= 1:
            return True

        return False


def update_last_active(user_id):
    now = datetime.now()
    activity_state[user_id] = {"last_active": now}

def get_lonely_score(user_id):
    """最後の会話から経過時間で寂しさスコアを返す"""
    now = datetime.now()
    last = activity_state.get(user_id, {}).get("last_active", now)
    delta = now - last
    hours = delta.total_seconds() / 3600
    return min(int(hours), 5)  # 最大5