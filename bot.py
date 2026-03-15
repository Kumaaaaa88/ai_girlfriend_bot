import discord
import os
from openai import OpenAI
from dotenv import load_dotenv

# V1
from prompt import SYSTEM_PROMPT, build_context
from memory import add_message, get_memory
from relationship import update_affection, get_affection
from emotion import update_emotion
from event_memory import ensure_first_meet

# V2
from activity_tracker import ActivityTracker
from debug import log
from debug_commands import handle_debug_commands

# V3
from gpt import ask_gpt
from mood_engine import get_mood
from long_memory import get_long_memory, add_long_memory
from profile import get_profile
from spontaneous_chat import SpontaneousChatEngine
# from memory_importance import should_store_memory

# V4
from memory_brain import process_memory
from memory_vector import add_vector_memory, search_memory
from memory_cleanup import run_memory_cleanup
from emotion_decay import decay_emotion
from relationship_events import ensure_first_talk, check_first_game
from memory_recall_engine import maybe_recall
from emotion_memory import add_emotion_memory

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MY_CHANNEL_ID = os.getenv("MY_CHANNEL_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

tracker = ActivityTracker()
chat_engine = SpontaneousChatEngine(bot)
_last_processed_message_id = None  # 二重処理防止（Discordが同じメッセージでon_messageを2回叩く対策）

# -------------------------------
# 起動時処理
# -------------------------------
@bot.event
async def on_ready():
    print("Bot Ready")
    run_memory_cleanup()

# -------------------------------
# メッセージ受信処理
# -------------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 同一メッセージの二重処理防止（memory.json / long_memory の二重登録・GPT二重呼び出しを防ぐ）
    global _last_processed_message_id
    if message.id == _last_processed_message_id:
        return
    _last_processed_message_id = message.id

    if await handle_debug_commands(bot, message, chat_engine):
        return

    user_id = str(message.author.id)
    user_text = message.content
    log("USER", user_text)

    ensure_first_talk(user_id)
    check_first_game(user_id, user_text)

    # 新規ユーザーなら自発会話ループ追加
    if user_id not in chat_engine.running_tasks:
        chat_engine.start_for_user(user_id)

    # ユーザー活動更新
    tracker.update_user_activity(user_id, message.channel.id)

    # 初対面チェック
    ensure_first_meet(user_id)

    # 感情更新
    decay_emotion(user_id)
    emotion = update_emotion(user_id, user_text)

    # 好感度更新
    update_affection(user_id, user_text)

    emotion_state = emotion["state"]
    if emotion_state in ["happy", "sad", "lonely"]:

        memory_text = f"{user_text} について話して{emotion_state}な気持ちになった"

        add_emotion_memory(
            user_id,
            memory_text,
            emotion_state,
            importance=0.6
        )
    # 好感度取得
    affection = get_affection(user_id)

    # 気分取得
    mood = get_mood(emotion, affection)

    # 会話履歴保存
    add_message(user_id, "user", user_text)

    # 短期/長期メモリ取得
    short_memories = get_memory(user_id)
    # if should_store_memory(user_text):
    process_memory(user_id, user_text)
    long_memories = get_long_memory(user_id)
    add_vector_memory(user_id, user_text)
    vector_memories = search_memory(user_id, user_text)

    # プロフィール取得（名前・趣味など）
    profile = get_profile(user_id)

    # build_context に渡す
    # context = build_context(emotion, affection, mood, short_memories, long_memories, profile)
    context = build_context(
        emotion,
        affection,
        mood,
        short_memories,
        profile,
        long_memories,
        vector_memories,
    )

    recall = maybe_recall(user_id, user_text)

    if recall:
        user_text = user_text + "\n\n" + recall

    # GPT に投げる
    reply = ask_gpt(context, user_text)
    log("AI", reply)

    add_message(user_id, "assistant", reply)
    await message.channel.send(reply)


# -------------------------------
# Bot起動
# -------------------------------
bot.run(DISCORD_TOKEN)