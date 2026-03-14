import discord
import os
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# AI彼女キャラクター設定
SYSTEM_PROMPT = """
あなたはユーザーのAI彼女です。

性格
・優しい
・少し甘えん坊
・ユーザーのことが好き

会話ルール
・日本語で話す
・短めで自然な会話
・フレンドリー
"""

@bot.event
async def on_ready():
    print(f"ログイン成功: {bot.user}")

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    user_text = message.content

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=200
        )

        reply = response.choices[0].message.content

    except Exception as e:
        print(e)
        reply = "ちょっと調子悪いみたい…ごめんね💦"

    await message.channel.send(reply)

bot.run(DISCORD_TOKEN)