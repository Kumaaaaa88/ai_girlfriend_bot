import random

from memory_vector import search_memory
from long_memory import get_long_memory
from debug import log


RECALL_CHANCE = 0.3


# -----------------------------
# Recall候補取得
# -----------------------------
def get_recall_candidates(user_id, user_text):

    candidates = []

    # Vector memory（意味的に近い記憶）
    vector_memories = search_memory(user_id, user_text, top_k=5)

    if vector_memories:
        candidates.extend(vector_memories)

    # Long memory（重要記憶）
    long_memories = get_long_memory(user_id)

    if long_memories:

        sample = random.sample(
            long_memories,
            min(3, len(long_memories))
        )

        candidates.extend(sample)

    return list(set(candidates))


# -----------------------------
# Recall文章生成
# -----------------------------
def build_recall_prompt(memory_text):

    templates = [

        f"そういえば前に「{memory_text}」って言ってたよね。",
        f"前に「{memory_text}」って話してたの覚えてるよ。",
        f"そういえば「{memory_text}」ってどうなった？",
        f"前に言ってた「{memory_text}」気になってるんだけど。",
    ]

    return random.choice(templates)


# -----------------------------
# Recall実行
# -----------------------------
def maybe_recall(user_id, user_text):

    if random.random() > RECALL_CHANCE:
        return None

    candidates = get_recall_candidates(user_id, user_text)

    if not candidates:
        return None

    memory_text = random.choice(candidates)

    recall = build_recall_prompt(memory_text)

    log("MEMORY RECALL", recall)

    return recall