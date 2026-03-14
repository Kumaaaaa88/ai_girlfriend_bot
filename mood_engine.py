import datetime


def get_mood(emotion, affection):
    """
    emotion: emotion.py の get_emotion / update_emotion が返す dict
        {
        "state": "normal" | "happy" | "sad" | "lonely" | "jealous",
        "level": 0-5,
        "updated_at": ...
        }
    affection: 好感度（0-100 想定）
    """

    state = emotion.get("state", "normal")
    level = emotion.get("level", 0)

    hour = datetime.datetime.now().hour

    # 夜はロマンチック（感情が落ち着いていて、好感度が高いとき）
    if hour >= 22 and affection is not None and affection > 60 and state in ["normal", "happy"]:
        return "romantic"

    # 感情の種類とレベルから気分を判定
    # level は 0-5 なので、3 以上を「かなり強い」とみなす
    if state == "lonely" and level >= 3:
        return "lonely"

    if state == "jealous" and level >= 3:
        return "jealous"

    if state == "happy" and level >= 3:
        return "cheerful"

    if state == "sad" and level >= 3:
        return "down"

    return "normal"