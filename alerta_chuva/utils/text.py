def parser_float(text: str) -> float | None:
    if isinstance(text, float):
        return text
    if text == "ND" or not text:
        return None
    return float(text.strip().replace(",", "."))
