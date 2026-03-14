import random
import asyncio
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv
import os

from emotion import get_emotion
from relationship import get_affection
from memory import get_memory, add_message
from long_memory import get_long_memory
from prompt import build_context
from mood_engine import get_mood
from activity_tracker import ActivityTracker
from profile import get_profile

# v4
from memory_vector import search_memory

from debug import log

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MY_CHANNEL_ID = os.getenv("MY_CHANNEL_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

tracker = ActivityTracker()

# -------------------------------
# フォールバック話題
# -------------------------------
FALLBACK_TOPICS = [
    "今日どうだった？",
    "最近ゲームしてる？",
    "ちゃんと休めてる？",
    "ご飯食べた？",
    "最近楽しいことあった？",
    "ねえねえ、今何してるの？",
    "今日疲れてない？",
]

# -------------------------------
# 話題生成
# -------------------------------
def generate_topic(user_id):

    emotion = get_emotion(user_id)
    # affection = get_affection(user_id)
    memories = get_long_memory(user_id)
    profile = get_profile(user_id)

    # memory話題
    if memories and random.random() < 0.4:
        memory = random.choice(memories)
        return f"ねえ、前に話してた「{memory}」どうなった？"

    # hobby話題
    hobby = profile.get("hobby")
    if hobby and random.random() < 0.4:
        return f"ねえねえ、最近{hobby}してる？"

    # 感情話題
    state = emotion["state"]

    if state == "lonely":
        return "ねえ…ちょっと寂しくなっちゃった"

    if state == "happy":
        return "ねえねえ、今日ちょっといい気分なんだ〜"

    # fallback
    return random.choice(FALLBACK_TOPICS)

# -------------------------------
# SpontaneousChatEngine クラス
# -------------------------------
class SpontaneousChatEngine:
    def __init__(self, bot_client):
        self.bot = bot_client
        self.running_tasks = {}

    async def maybe_spontaneous_chat(self, user_id):
        """条件に応じて自発会話を生成"""
        # 1. ユナの状態
        emotion = get_emotion(user_id)
        affection = get_affection(user_id)
        mood = get_mood(emotion, affection)

        # 2. メモリ
        short_memories = get_memory(user_id)
        long_memories = get_long_memory(user_id)

        # プロフィール
        profile = get_profile(user_id)

        # 3. 寂しさスコア
        lonely_score = tracker.get_lonely()

        # 4. 発話確率
        chance = min(0.2 + 0.15 * lonely_score + 0.1 * (affection / 100), 0.8)
        if random.random() >= chance:
            return None  # 発話しない

        # 5. 話題選択
        user_message = generate_topic(user_id)
        vector_memories = search_memory(user_id, user_message)

        # 6. context生成
        context = build_context(emotion, affection, mood, short_memories, profile, long_memories, vector_memories)

        # 7. GPT呼び出し
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            print("自発会話生成失敗:", e)
            reply = user_message  # フォールバック

        # 8. 短期メモリ保存
        add_message(user_id, "assistant", reply)

        # 9. 最終アクティブ時間更新
        tracker.update_user_activity(user_id, MY_CHANNEL_ID)

        # 10. Discordに送信
        channel = self.bot.get_channel(int(MY_CHANNEL_ID))
        if channel:
            await channel.send(reply)

        return reply

    # TODO：テスト用の関数　maybe_spontaneous_chatに修正が入る場合ここも修正
    async def force_chat(self, user_id):
        """必ず1回分の会話を生成（テスト用）"""
        # 1. ユナの状態
        emotion = get_emotion(user_id)
        affection = get_affection(user_id)
        mood = get_mood(emotion, affection)

        # 2. メモリ
        short_memories = get_memory(user_id)
        long_memories = get_long_memory(user_id)

        # プロフィール
        profile = get_profile(user_id)

        # 3. 話題選択（確率チェックはしない）
        user_message = generate_topic(user_id)

        # 4. context生成
        context = build_context(emotion, affection, mood, short_memories, long_memories, profile)

        # 5. GPT呼び出し
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.8
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            print("強制会話生成失敗:", e)
            reply = user_message  # フォールバック

        return reply

    async def spontaneous_loop(self, user_id, interval=600):
        """10分ごとに自発会話チェック"""
        while True:
            await self.maybe_spontaneous_chat(user_id)
            await asyncio.sleep(interval)

    def start_for_user(self, user_id, interval=600):
        """特定ユーザーのループを開始"""
        if user_id in self.running_tasks:
            return  # 既にループ中
        task = asyncio.create_task(self.spontaneous_loop(user_id, interval))
        self.running_tasks[user_id] = task

    def start(self, user_ids, interval=600):
        """複数ユーザーの自発会話ループ開始"""
        for user_id in user_ids:
            self.start_for_user(user_id, interval)