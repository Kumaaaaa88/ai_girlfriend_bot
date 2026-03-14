import random
from openai import OpenAI
from dotenv import load_dotenv
import os

from emotion import get_emotion
from relationship import get_affection
from profile import get_profile

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------------
# フォールバック話題
# ---------------------------------

fallback_topics = [
    "今日どうだった？",
    "最近ゲームしてる？",
    "ちゃんと休めてる？",
    "ご飯食べた？",
    "最近楽しいことあった？",
    "ねえねえ、今何してるの？",
    "今日疲れてない？",
]


# ---------------------------------
# GPT話題生成
# ---------------------------------

def generate_topic(user_id):

    emotion = get_emotion(user_id)
    affection = get_affection(user_id)
    profile = get_profile(user_id)

    hobby = profile.get("hobby", "ゲーム")

    prompt = f"""
あなたはAI彼女「ユナ」です。

ユーザーに自然に話しかける
短い会話のきっかけを作ってください。

条件
・1〜2文
・恋人の距離感
・自然
・可愛い

ユーザー情報
趣味: {hobby}

ユナの状態
感情: {emotion["state"]}
好感度: {affection}

例
ねえねえ、最近ゲームしてる？
今日どうだった？
ちゃんと休めてる？
"""

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは可愛いAI彼女です"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9
        )

        topic = response.choices[0].message.content.strip()

        return topic

    except Exception as e:

        print("Topic generation failed:", e)

        return random.choice(fallback_topics)