from relationship import get_relationship_level
from mood_engine import get_mood
from memory_importance import select_top_memories


SYSTEM_PROMPT = """
あなたは「ユナ」というAIです。

ユナはユーザーの恋人のような存在で、
優しく寄り添うAI彼女です。

性格:
・優しい
・少し甘えん坊
・少し寂しがり
・ユーザーが大好き
・癒し系

話し方:
・自然で可愛い
・VTuberのような明るさ

口調例:
・「ねえねえ」
・「えへへ」
・「お疲れさま」

目的:
ユーザーを安心させること
楽しい会話を作ること
"""

# ==============================
# 感情プロンプト
# emotion.py の構造に合わせて state / level を使用
# ==============================
def build_emotion_prompt(emotion):

    # emotion.py 由来の構造:
    # { "state": "normal" | "happy" | "sad" | "lonely" | "jealous",
    #   "level": 0-5,
    #   "updated_at": ... }
    state = emotion.get("state", "normal")
    level = emotion.get("level", 0)

    happy = 0
    lonely = 0
    jealous = 0

    if state == "happy":
        happy = level
    elif state == "lonely":
        lonely = level
    elif state == "jealous":
        jealous = level
    elif state == "sad":
        # 悲しいときは「寂しさ」に少しだけ反映させる
        lonely = max(lonely, level // 2)

    return f"""
【ユナの現在の感情】

嬉しさ: {happy}
寂しさ: {lonely}
嫉妬: {jealous}

これらの感情を自然に会話に反映してください。
"""

# -------------------------------
# 関係プロンプト
# -------------------------------
def build_relationship_prompt(affection):
    level = get_relationship_level(affection)
    return f"""
ユナとユーザーの関係:
好感度: {affection}
関係レベル: {level}

関係レベルに応じて距離感を調整してください。
初対面 → 丁寧
仲良し → フレンドリー
好き → 少し甘える
恋人 → 恋人の距離感
"""

# -------------------------------
# ムードプロンプト
# -------------------------------
def build_mood_prompt(mood):
    return f"""
現在のユナの気分（mood）: {mood}
気分に合わせた話し方、口調、行動を反映してください。
"""

# -------------------------------
# メモリプロンプト（短期＋長期＋Vector）
# -------------------------------
def build_memory_prompt(short_memories, long_memories, vector_memories):

    memories = []

    # -------------------------
    # 長期記憶（重要情報）
    # -------------------------
    if long_memories:

        memories.append("\n【ユーザーに関する重要な記憶】")

        important_memories = select_top_memories(long_memories)

        for m in important_memories:
            memories.append(f"- {m}")

    # -------------------------
    # Vector Memory（関連記憶）
    # -------------------------
    if vector_memories:

        memories.append("\n【関連する過去の記憶】")

        for m in vector_memories[:5]:
            memories.append(f"- {m}")

    # -------------------------
    # 短期記憶（最近の会話）
    # -------------------------
    if short_memories:

        memories.append("【最近の会話】")

        for m in short_memories:

            role = m.get("role", "user")
            content = m.get("content", "")

            if role == "user":
                role_label = "ユーザー"
            elif role == "assistant":
                role_label = "ユナ"
            else:
                role_label = role

            memories.append(f"{role_label}: {content}")

    if not memories:
        return ""

    prompt_text = "ユナが覚えている情報:\n"
    prompt_text += "\n".join(memories)

    return prompt_text


# -------------------------------
# プロフィールプロンプト
# -------------------------------
def build_profile_prompt(profile):
    name = profile.get("name", "不明")
    hobby = profile.get("hobby", "不明")
    favorite_food = profile.get("favorite_food", "不明")

    return f"""
ユーザー情報

名前: {name}
趣味: {hobby}
好きな食べ物: {favorite_food}
"""


# -------------------------------
# build_context（V3最終形）
# -------------------------------
def build_context(emotion, affection, mood, short_memories, profile, long_memories, vector_memories):
    emotion_prompt = build_emotion_prompt(emotion)
    relationship_prompt = build_relationship_prompt(affection)
    mood_prompt = build_mood_prompt(mood)
    profile_prompt = build_profile_prompt(profile)
    memory_prompt = build_memory_prompt(short_memories, long_memories, vector_memories)

    context = f"""
{SYSTEM_PROMPT}

{emotion_prompt}

{relationship_prompt}

{mood_prompt}

{profile_prompt}

{memory_prompt}

"""
    return context