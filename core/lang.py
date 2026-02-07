def detect_lang(text: str) -> str:
    for ch in text:
        if "\u0980" <= ch <= "\u09FF":
            return "bn"
    return "en"
