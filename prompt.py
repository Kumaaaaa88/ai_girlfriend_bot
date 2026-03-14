from relationship import get_relationship_level
from mood_engine import get_mood

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
# メモリプロンプト（短期＋長期）
# -------------------------------
def build_memory_prompt(short_memories, long_memories):
    all_memories = []

    # 短期
    for m in short_memories:
        role = m.get("role", "user")
        content = m.get("content", "")
        all_memories.append(f"[{role}] {content}")

    # 長期
    for m in long_memories:
        all_memories.append(f"[long-term] {m}")

    if not all_memories:
        return ""

    prompt_text = "ユーザーに関する記憶:\n"
    for mem in all_memories:
        prompt_text += f"- {mem}\n"

    return prompt_text

# -------------------------------
# build_context（V3最終形）
# -------------------------------
def build_context(emotion, affection, mood, short_memories, long_memories):
    emotion_prompt = build_emotion_prompt(emotion)
    relationship_prompt = build_relationship_prompt(affection)
    mood_prompt = build_mood_prompt(mood)
    memory_prompt = build_memory_prompt(short_memories, long_memories)

    context = f"""
{SYSTEM_PROMPT}

{emotion_prompt}

{relationship_prompt}

{mood_prompt}

{memory_prompt}
"""
    return context