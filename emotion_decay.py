import time

from emotion import get_emotion, save_emotion


# -----------------------------
# 感情減衰設定
# -----------------------------

DECAY_INTERVAL = 600  # 10分


# -----------------------------
# 感情減衰処理
# -----------------------------

def decay_emotion(user_id):

    emotion = get_emotion(user_id)

    state = emotion.get("state", "normal")
    level = emotion.get("level", 0)
    updated_at = emotion.get("updated_at", time.time())

    now = time.time()
    elapsed = now - updated_at

    # まだ減衰タイミングでない
    if elapsed < DECAY_INTERVAL:
        return emotion

    # 減衰回数
    steps = int(elapsed // DECAY_INTERVAL)

    # -----------------------------
    # 感情変化
    # -----------------------------

    if state == "happy":

        level -= steps

        if level <= 0:
            state = "normal"
            level = 0

    elif state == "jealous":

        level -= steps

        if level <= 0:
            state = "normal"
            level = 0

    elif state == "sad":

        level -= steps

        if level <= 0:
            state = "normal"
            level = 0

    elif state == "lonely":

        # 寂しさは逆に増える
        level += steps

        if level > 5:
            level = 5

    # normal は変化なし

    emotion["state"] = state
    emotion["level"] = level
    emotion["updated_at"] = now

    save_emotion(user_id, emotion)

    return emotion