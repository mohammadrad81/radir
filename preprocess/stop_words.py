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
    "است",
    "بود",
    "شد",
    "اما"
    "ای",
    "ها",
    "و",
}


def is_stop_word(token: str) -> bool:
    return token in STOP_WORDS


def remove_stop_words(tokens: list[str]):
    return [token for token in tokens if token not in STOP_WORDS]
