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
from discord.ext import tasks
from topic_generator import generate_topic
from spontaneous_chat import SpontaneousChatEngine


# V3
from gpt import ask_gpt
from mood_engine import get_mood
from long_memory import get_long_memory
from prompt import build_memory_prompt

from debug import log
from debug_commands import handle_debug_commands

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

@bot.event
async def on_ready():
    print("Bot Ready")
    chat_engine.start()

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if await handle_debug_commands(bot, message):
        return

    user_id = str(message.author.id)
    user_text = message.content
    log("USER", user_text)

    tracker.update_user_activity(
        user_id,
        message.channel.id
    )

    # 初対面チェック
    ensure_first_meet(user_id)

    # 感情更新
    emotion = update_emotion(user_id, user_text)

    # 好感度更新
    update_affection(user_id, user_text)

    # 好感度取得
    affection = get_affection(user_id)

    # 気分取得
    mood = get_mood(emotion, affection)

    # 会話履歴保存
    add_message(user_id, "user", user_text)

    # 短期と長期を取得
    short_memories = get_memory(user_id)
    long_memories = get_long_memory(user_id)

    # build_context に渡す
    context = build_context(
        emotion,
        affection,
        mood,
        short_memories,
        long_memories
    )

    reply = ask_gpt(context, user_text)

    log("AI", reply)

    add_message(user_id, "assistant", reply)

    await message.channel.send(reply)

bot.run(DISCORD_TOKEN)