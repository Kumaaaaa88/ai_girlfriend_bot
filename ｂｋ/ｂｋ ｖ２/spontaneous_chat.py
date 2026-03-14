import random
import datetime
from discord.ext import tasks

from activity_tracker import ActivityTracker
from relationship import get_affection
from topic_generator import generate_topic

# V3
from long_memory import get_long_memory
from prompt import build_context
from mood_engine import get_mood
from activity_tracker import get_lonely_score
from gpt import ask_gpt

from debug import log

tracker = ActivityTracker()


class SpontaneousChatEngine:

    def __init__(self, bot):

        self.bot = bot

    # -------------------------
    # 時間帯判定
    # -------------------------

    def get_time_period(self):

        hour = datetime.datetime.now().hour

        if 5 <= hour < 10:
            return "morning"

        if 10 <= hour < 18:
            return "day"

        if 18 <= hour < 24:
            return "evening"

        return "night"

    # -------------------------
    # 曜日判定
    # -------------------------

    def is_weekend(self):

        weekday = datetime.datetime.now().weekday()

        return weekday >= 5

    # -------------------------
    # 会話確率計算
    # -------------------------

    def conversation_probability(self, affection, lonely):

        base = 0.1

        base += affection / 200

        base += lonely * 0.05

        return min(base, 0.8)

    # -------------------------
    # 時間帯フィルタ
    # -------------------------

    def time_filter(self):

        period = self.get_time_period()

        if period == "night":

            if random.random() < 0.8:
                return False

        return True

    # -------------------------
    # メッセージ生成
    # -------------------------

    def build_message(self, user_id):

        topic = generate_topic(user_id)

        return topic

    # -------------------------
    # 自発会話判定
    # -------------------------

    def should_chat(self, user_id):

        affection = get_affection(user_id)

        lonely = tracker.update_lonely()

        if lonely == 0:
            return False

        probability = self.conversation_probability(
            affection,
            lonely
        )

        if random.random() > probability:
            return False

        if not self.time_filter():
            return False

        return True

    # -------------------------
    # 会話実行
    # -------------------------

    async def run(self):

        data = tracker.load()

        user_id = data["last_user_id"]
        channel_id = data["last_channel_id"]

        if not user_id:
            return

        if not self.should_chat(user_id):
            return

        channel = self.bot.get_channel(channel_id)

        if not channel:
            return

        message = self.build_message(user_id)

        await channel.send(message)

    # -------------------------
    # ループ開始
    # -------------------------

    def start(self):

        self.loop.start()

    # -------------------------
    # 定期チェック
    # -------------------------

    @tasks.loop(minutes=10)
    async def loop(self):
        log("loop実行")

        await self.run()

def maybe_spontaneous_chat(user_id, emotion, short_memories):
    affection = get_affection(user_id)
    mood = get_mood(emotion, affection)
    long_memories = get_long_memory(user_id)
    
    # 寂しさスコア
    lonely_score = get_lonely_score(user_id)
    
    # 会話確率を計算（例: lonely_scoreが高いほど発言確率UP）
    chance = min(0.2 + 0.15 * lonely_score, 0.8)
    
    if random.random() < chance:
        # 話題選択: 長期メモリに基づいて話題を決定
        if long_memories:
            topic = random.choice(long_memories)
            user_message = f"ねえ、前に話してた {topic} のこと覚えてる？"
        else:
            user_message = "ねえ、最近どうだった？"
        
        # context生成
        context = build_context(emotion, affection, mood, short_memories, long_memories)
        
        # GPT呼び出し
        reply = ask_gpt(context, user_message)
        
        return reply
    return None