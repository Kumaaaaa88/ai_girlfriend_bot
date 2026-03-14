def should_store_memory(text):

    keywords = [
        "好き",
        "趣味",
        "仕事",
        "誕生日",
        "ゲーム",
        "住んで"
    ]

    for k in keywords:
        if k in text:
            return True

    if len(text) > 40:
        return True

    return False