import re
from long_memory import add_long_memory


# -----------------------------
# 保存対象キーワード
# -----------------------------

IMPORTANT_PATTERNS = [
    r"好き",
    r"嫌い",
    r"趣味",
    r"仕事",
    r"学校",
    r"誕生日",
    r"住んで",
    r"ゲーム",
]


# -----------------------------
# 保存しない会話
# -----------------------------

IGNORE_PATTERNS = [
    r"おはよう",
    r"こんにちは",
    r"こんばんは",
    r"眠い",
    r"疲れた",
    r"ただいま",
]


# -----------------------------
# 保存するか判断
# -----------------------------

def should_store_memory(text):

    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, text):
            return False

    for pattern in IMPORTANT_PATTERNS:
        if re.search(pattern, text):
            return True

    return False


# -----------------------------
# 記憶抽出
# -----------------------------

def extract_memory(text):

    if "好き" in text:
        return text

    if "趣味" in text:
        return text

    if "仕事" in text:
        return text

    if "ゲーム" in text:
        return text

    if "誕生日" in text:
        return text

    return None


# -----------------------------
# メモリ処理
# -----------------------------

def process_memory(user_id, text):

    if not should_store_memory(text):
        return

    memory = extract_memory(text)

    if memory:
        add_long_memory(user_id, memory)