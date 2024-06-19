ENGLISH_NUMERICS = list(str(x) for x in range(10))
PERSIAN_NUMERICS = [
    "۰",
    "١",
    "۲",
    "۳",
    "۴",
    "۵",
    "۶",
    "۷",
    "۸",
    "۹"
]


def remove_tanvin(text: str) -> str:
    text = text.replace("\u064b", "")
    text = text.replace("\u064c", "")
    text = text.replace("\u064d", "")
    return text


def remove_erab(text: str) -> str:
    text = text.replace("\u064f", "")
    text = text.replace("\u064e", "")
    text = text.replace("\u0650", "")
    return text


def remove_punctuations(text: str) -> str:
    text = text.replace("#", " ")
    text = text.replace("«", " ")
    text = text.replace("»", " ")
    text = text.replace(":", " ")
    text = text.replace("؛", " ")
    text = text.replace("،", " ")
    text = text.replace(",", " ")
    text = text.replace("-", " ")
    text = text.replace("!", " ")
    text = text.replace("؟", " ")
    text = text.replace("\u061F", " ")
    text = text.replace("،", " ")
    text = text.replace(":", " ")
    text = text.replace(";", " ")
    text = text.replace("\n", " ")
    text = text.replace(".", " ")
    text = text.replace("/", " ")
    # " - '
    text = text.replace("\u0022", " ")
    text = text.replace("\u0027", " ")
    return text


def remove_half_space(text: str) -> str:
    text = text.replace("\u200c", " ")
    text = text.replace("\u200d", " ")
    return text


def english_numerics_to_persian(text: str) -> str:
    for en, per in zip(ENGLISH_NUMERICS, PERSIAN_NUMERICS):
        text = text.replace(en, per)
    return text


def arabic_to_persian_marks(text: str) -> str:
    # ک عربی
    text = text.replace("\u0643", "\u06a9")
    # ی عربی
    text = text.replace("\u064a", "\u06cc")
    # تشدید
    text = text.replace("\u0651", "")
    #ۀ
    text = text.replace("\u06C0", "")
    text = text.replace("\u0621", "")

    text = text.replace("آ", "ا")
    text = text.replace(" ی ", "ی ")
    #ئ
    text = text.replace("ئ", "ئ")

    return text


def normalize(text):
    text = remove_tanvin(text)
    text = remove_erab(text)
    text = remove_punctuations(text)
    text = remove_half_space(text)
    text = arabic_to_persian_marks(text)
    text = english_numerics_to_persian(text)
    text = text.strip()
    return text
