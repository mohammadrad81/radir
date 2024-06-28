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
    "ای",
    "های"
}

REPEATING_WORDS = {
"به" ,
"فارس" ,
"پیام" ,
"انتهای" ,
"در" ,
"و" ,
"خبرگزاری" ,
"از" ,
"این" ,
"با" ,
"گزارش" ,
"را" ,
"که" ,
"است" ,
"کرد" ,
"برای" ,
"شد" ,
"تا" ,
"وی" ,
"خبرنگار" ,
"یک" ,
"بر" ,
"خود" ,
"داشت" ,
"بود" ,
"گفت" ,
"شده" ,
"هم" ,
"تیم" ,
"ان" ,
"قرار" ,
"شود" ,
"امروز" ,
"دارد" ,
"باید" ,
"داد" ,
"اما" ,
"اظهار" ,
"کشور" ,
"اسلامی" ,
"کند" ,
"ادامه" ,
"می‌شود" ,
"حضور" ,
"ما" ,
"بازی" ,
"دو" ,
"اینکه" ,
"سال" ,
"عنوان" ,
}


def is_stop_word(token: str) -> bool:
    return token in STOP_WORDS

def is_repeating_word(token: str) -> bool:
    return token in REPEATING_WORDS

def is_useless_word(token: str) -> bool:
    return is_stop_word(token) or is_repeating_word(token)

def remove_useless_words(tokens: list[str]) -> list[str]:
    return [token for token in tokens if not is_useless_word(token)]
