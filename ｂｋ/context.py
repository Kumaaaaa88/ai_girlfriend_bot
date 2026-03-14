from prompt import SYSTEM_PROMPT, build_emotion_prompt
from memory import get_memory
# from emotion import get_emotion
from emotion import build_emotion_context
from profile import get_profile

from relationship import get_affection
from prompt import build_relationship_prompt

from event_memory import get_events

# コンテキスト
def build_context(user_id, user_text):

    messages = []

    # AI彼女人格
    messages.append({
        "role": "system",
        "content": SYSTEM_PROMPT
    })

    # emotion = get_emotion(user_id)
    # emotion_prompt = build_emotion_prompt(emotion)
    emotion_prompt = build_emotion_context(user_id)

    # 感情状態
    messages.append({
        "role": "system",
        "content": emotion_prompt
    })
    
    affection = get_affection(user_id)

    relationship_prompt = build_relationship_prompt(affection)

    messages.append({
        "role": "system",
        "content": relationship_prompt
    })

    # ユーザープロフィール
    profile = get_profile(user_id)

    profile_prompt = f"""
ユーザー情報

名前: {profile.get("name","不明")}
趣味: {profile.get("hobby","不明")}
好きな食べ物: {profile.get("favorite_food","不明")}
"""

    messages.append({
        "role": "system",
        "content": profile_prompt
    })

    events = get_events(user_id)

    event_text = ""

    for e in events[-5:]:
        event_text += f"{e['date']} : {e['value']}\n"

    event_prompt = f"""
ユナとユーザーの思い出

{event_text}

思い出を自然に会話に使ってください。
"""
    messages.append({
        "role": "system",
        "content": event_prompt
    })   

    # 会話履歴
    history = get_memory(user_id)
    messages += history

    # 今のユーザー発言
    messages.append({
        "role": "user",
        "content": user_text
    })

    return messages