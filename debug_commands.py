import json

from emotion import get_emotion
from relationship import get_affection
from memory import get_memory
from long_memory import get_long_memory
from mood_engine import get_mood
from profile import get_profile
from activity_tracker import ActivityTracker

tracker = ActivityTracker()


async def handle_debug_commands(bot, message, chat_engine):

    if not message.content.startswith("!"):
        return False

    user_id = str(message.author.id)
    cmd = message.content.lower()

    # -----------------------
    # 感情確認 !emotion
    # -----------------------
    if cmd == "!emotion":

        emotion = get_emotion(user_id)
        affection = get_affection(user_id)

        await message.channel.send(
            f"【ユナの感情】\n"
            f"状態: {emotion['state']}\n"
            f"感情スコア: {emotion['level']}"
        )

        return True

    # -----------------------
    # 好感度 affection
    # -----------------------
    if cmd == "!affection":

        affection = get_affection(user_id)

        await message.channel.send(
            f"【好感度】\n現在の好感度: {affection}"
        )

        return True

    # -----------------------
    # ユナの気分 !mood
    # -----------------------
    if cmd == "!mood":

        emotion = get_emotion(user_id)
        affection = get_affection(user_id)
        mood = get_mood(emotion, affection)

        await message.channel.send(
            f"【ユナの気分】\n現在のMood: {mood}"
        )

        return True

    # -----------------------
    # 寂しさ !lonely
    # -----------------------
    if cmd == "!lonely":

        lonely = tracker.get_lonely()

        await message.channel.send(
            f"【寂しさ】\n寂しさスコア: {lonely}"
        )

        return True

    # -----------------------
    # 短期記憶 !memory
    # -----------------------
    if cmd == "!memory":

        mem = get_memory(user_id)

        if not mem:
            await message.channel.send("短期記憶はまだありません")
            return True

        text = "\n".join(
            [f"{m['role']} : {m['content']}" for m in mem[-10:]]
        )

        await message.channel.send(
            f"【短期記憶（最近の会話）】\n{text}"
        )

        return True

    # -----------------------
    # 長期記憶 !long
    # -----------------------
    if cmd == "!long":

        mem = get_long_memory(user_id)

        if not mem:
            await message.channel.send("長期記憶はまだありません")
            return True

        text = "\n".join(mem[-10:])

        await message.channel.send(
            f"【長期記憶】\n{text}"
        )

        return True

    # -----------------------
    # プロフィール !profile
    # -----------------------
    if cmd == "!profile":

        profile = get_profile(user_id)

        text = json.dumps(profile, indent=2, ensure_ascii=False)

        await message.channel.send(
            f"【ユーザープロフィール】\n```json\n{text}\n```"
        )

        return True

    # -----------------------
    # 状態まとめ !status
    # -----------------------
    if cmd == "!status":

        emotion = get_emotion(user_id)
        affection = get_affection(user_id)
        mood = get_mood(emotion, affection)
        lonely = tracker.get_lonely()
        hours = tracker.hours_since_last_message()

        await message.channel.send(
            f"""
【ユナの現在状態】

感情: {emotion['state']}
感情スコア: {emotion['level']}
好感度: {affection}
Mood: {mood}
寂しさ: {lonely}
最後の会話:{hours:.1f}時間前"
"""
        )

        return True

    # -----------------------
    # 強制自発会話 !spontaneous
    # -----------------------
    if cmd == "!spontaneous":

        await message.channel.send("自発会話テストを開始します…")

        reply = await chat_engine.maybe_spontaneous_chat(user_id)

        if reply:
            await message.channel.send(f"ユナが自発会話しました！\n{reply}")
        else:
            await message.channel.send("発話条件を満たさず会話は発生しませんでした")

        return True

    # -----------------------
    # 会話生成テスト talk
    # -----------------------
    if cmd == "!talk":

        await message.channel.send("会話生成テストを実行します")

        # 確率に関係なく必ず1回生成
        # reply = await chat_engine.maybe_spontaneous_chat(user_id)
        reply = await chat_engine.force_chat(user_id)


        if reply:
            await message.channel.send(reply)

        return True

    # -----------------------
    # 開発者デバッグ !debug
    # -----------------------
    if cmd == "!debug":

        emotion = get_emotion(user_id)
        affection = get_affection(user_id)
        mood = get_mood(emotion, affection)
        lonely = tracker.get_lonely()
        mem = get_memory(user_id)
        long_mem = get_long_memory(user_id)

        await message.channel.send(
            f"""
【デバッグ情報】

感情: {emotion}
好感度: {affection}
Mood: {mood}
寂しさ: {lonely}

短期記憶数: {len(mem)}
長期記憶数: {len(long_mem)}
"""
        )

        return True

    return False