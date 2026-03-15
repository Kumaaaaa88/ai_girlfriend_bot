import re


# -----------------------------
# 重要度スコア
# -----------------------------

def calculate_importance(text):

    score = 1

    # 超重要
    if re.search(r"誕生日|名前|住んで", text):
        score += 5

    # 重要
    if re.search(r"仕事|学校|趣味", text):
        score += 3

    # 興味
    if re.search(r"好き|ゲーム|映画", text):
        score += 2

    # 感情
    if re.search(r"悲しい|辛い|嬉しい", text):
        score += 2

    return score


# -----------------------------
# 上位記憶だけ残す
# -----------------------------

def select_top_memories(memories, top_k=10):

    scored = []

    for m in memories:

        score = calculate_importance(m)

        scored.append({
            "text": m,
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:top_k]