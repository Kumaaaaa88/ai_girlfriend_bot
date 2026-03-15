import os
import json
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

VECTOR_FILE = "data/vector_memory.json"


# -----------------------------
# ファイル読み込み
# -----------------------------

def load_vectors():

    if not os.path.exists(VECTOR_FILE):
        return []

    with open(VECTOR_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------
# 保存
# -----------------------------

def save_vectors(data):

    with open(VECTOR_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -----------------------------
# embedding生成
# -----------------------------

def get_embedding(text):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


# -----------------------------
# vector保存
# -----------------------------

def add_vector_memory(user_id, text):

    vectors = load_vectors()

    embedding = get_embedding(text)

    vectors.append({
        "user_id": user_id,
        "text": text,
        "embedding": embedding
    })

    save_vectors(vectors)


# -----------------------------
# コサイン類似度
# -----------------------------

def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# -----------------------------
# 類似記憶検索
# -----------------------------

def search_memory(user_id, query, top_k=3):

    vectors = load_vectors()

    query_embedding = get_embedding(query)

    scored = []

    for item in vectors:

        if item["user_id"] != user_id:
            continue

        score = cosine_similarity(query_embedding, item["embedding"])

        scored.append((score, item["text"]))

    scored.sort(reverse=True)

    return [text for score, text in scored[:top_k]]