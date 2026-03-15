import os
import json
import numpy as np

VECTOR_MEMORY_FILE = "data/vector_memory.json"


# -----------------------------
# JSONロード
# -----------------------------

def load_vectors():

    if not os.path.exists(VECTOR_MEMORY_FILE):
        return []

    with open(VECTOR_MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# JSON保存
# -----------------------------

def save_vectors(data):

    with open(VECTOR_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -----------------------------
# コサイン類似度
# -----------------------------

def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# -----------------------------
# 重複削除
# -----------------------------

def deduplicate_vectors(threshold=0.92):

    vectors = load_vectors()

    cleaned = []

    for item in vectors:

        duplicate = False

        for kept in cleaned:

            if item["user_id"] != kept["user_id"]:
                continue

            score = cosine_similarity(
                item["embedding"],
                kept["embedding"]
            )

            if score > threshold:
                duplicate = True
                break

        if not duplicate:
            cleaned.append(item)

    save_vectors(cleaned)

    return len(vectors), len(cleaned)