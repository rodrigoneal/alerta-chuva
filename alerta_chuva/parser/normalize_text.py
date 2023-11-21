def normalize_text(texts: list[str]) -> str:
    if len(texts) < 5:
        data = texts[2].split(" ", 1)[0]
        hora = texts[2].split(" ", 1)[1]
        texts.insert(2, data)
        texts[3] = hora
    normalized = [text.replace(" ", "").replace(".", ":") for text in texts]
    return " ".join(normalized)