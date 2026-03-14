from emotion import get_emotion
from relationship import get_affection
from activity_tracker import ActivityTracker
from topic_generator import generate_topic
from memory import get_memory

tracker = ActivityTracker()


async def handle_debug_commands(bot, message):

    user_id = str(message.author.id)

    # -------------------------
    # !status
    # -------------------------
    if message.content == "!status":

        emotion = get_emotion(user_id)
        affection = get_affection(user_id)
        lonely = tracker.get_lonely()
        hours = tracker.hours_since_last_message()

        text = f"""
📊 ユナの状態

感情: {emotion["state"]}
感情レベル: {emotion["level"]}

好感度: {affection}

寂しさ: {lonely}

最後の会話:
{hours:.1f}時間前
"""

        await message.channel.send(text)
        return True

    # -------------------------
    # !topic
    # -------------------------
    if message.content == "!topic":

        topic = generate_topic(user_id)

        await message.channel.send("🧠 話題生成テスト\n\n" + topic)

        return True

    # -------------------------
    # !lonely
    # -------------------------
    if message.content == "!lonely":

        lonely = tracker.get_lonely()

        await message.channel.send(f"現在の寂しさ: {lonely}")

        return True

    # -------------------------
    # !affection
    # -------------------------
    if message.content == "!affection":

        affection = get_affection(user_id)

        await message.channel.send(f"現在の好感度: {affection}")

        return True

    # -------------------------
    # !memory
    # -------------------------
    if message.content == "!memory":

        history = get_memory(user_id)

        text = "📚 最近の会話履歴\n\n"

        for m in history[-6:]:

            role = "ユーザー" if m["role"] == "user" else "ユナ"

            text += f"{role}: {m['content']}\n"

        await message.channel.send(text)

        return True

    # -------------------------
    # !force_chat
    # -------------------------
    if message.content == "!force_chat":

        topic = generate_topic(user_id)

        await message.channel.send(topic)

        return True

    return False