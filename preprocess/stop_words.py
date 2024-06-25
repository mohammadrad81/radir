STOP_WORDS = {
    "از",
    "با",
    "به",
    "بر",
    "برای",
    "درباره",
    "در",
    "یا",
    "ی",
    "که",
    "اینکه",
    "اما"
    "ای",
    "ها",
    "و",
    "را",
}


def is_stop_word(token: str) -> bool:
    return token in STOP_WORDS


def remove_stop_words(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token not in STOP_WORDS]
