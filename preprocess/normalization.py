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
PERSIAN_ABBREVIATIONS = [
    ("ره", "راه"),
    ("کوته", "کوتاه"),
    ("دگر", "دیگر"),
    ("چو", "چون"),
    ("ار", "اگر"),
    ("روبه", "روباه"),
    ("کنون", "اکنون"),
    ("گنه", "گناه"),
    ("دهن", "دهان"),
    ("پیرهن", "پیراهن"),
    ("برون", "بیرون"),
    ("ناجا", "نیروی انتظامی جمهوری اسلامی ایران"),
    ("نزاجا", "نیروی زمینی ارتش جمهوری اسلامی ایران"),
    ("ساواک", "سازمان اطلاعات و امنیت کشور"),
    ("سمپاد", "سازمان ملی پرورش استعداد های درخشان"),
    ("ق.ظ", "قبل ظهر"),
    ("ب.ظ", "بعد ظهر"),
    ("", ""),
    ("", ""),
    ("ج.ا.ا", "جمهوری اسلامی ایران"),
]

ENGLISH_ABBREVIATIONS = [
    ("A.S.A.P", "as soon as possible"),
    ("U.S.A", "united states of america"),
    ("USA", "united states of america"),
    ("IR", "islamic republic"),
    ("IRI", "islamic republic of iran"),
    ("IRIB", "islamic republic of iran broadcasting"),

]

def process_abbreviations(text: str):
    for short_form_list in [ENGLISH_ABBREVIATIONS, PERSIAN_ABBREVIATIONS]:
        for short_form, long_form in short_form_list:
            text.replace(
                " " + short_form + " ",
                " " + long_form + " "
            )
    return text

def remove_tanvin(text: str) -> str:
    text = text.replace("\u064b", "") # fathe tanvin
    text = text.replace("\u064c", "") # zamme tanvin
    text = text.replace("\u064d", "") # kasre tanvin
    return text


def remove_erab(text: str) -> str:
    text = text.replace("\u064f", "") # zamme
    text = text.replace("\u064e", "") # fathe
    text = text.replace("\u0650", "") # kasre
    text = text.replace("\u0652", "") # sukun
    text = text.replace("\u0670", "") # small superscript alef
    return text

def remove_endline_tab(text: str) -> str:
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    return text

def remove_meaningless_unicode_characters(text: str) -> str:
    text = text.replace("\u061F", " ") # arabic question mark
    text = text.replace("\u200F", " ") # left to right
    text = text.replace("\u200E", " ") # right to left
    text = text.replace("\u202B", " ") #right to left embedding
    text = text.replace("\u2069", " ") #Pop Directional Isolate character
    text = text.replace("\u202C", " ") #Pop Directional Formatting character
    text = text.replace("\u2067", " ") #right to left isolate
    text = text.replace("\u202A", " ") #left to right embedding
    return text

def remove_punctuations(text: str) -> str:
    text = text.replace("#", " ")
    text = text.replace("«", " ")
    text = text.replace("»", " ")
    text = text.replace("<", " ")
    text = text.replace(">", " ")
    text = text.replace("?", " ")
    text = text.replace(":", " ")
    text = text.replace("؛", " ")
    text = text.replace("،", " ")
    text = text.replace(",", " ")
    text = text.replace("-", " ")
    text = text.replace("!", " ")
    text = text.replace("؟", " ")
    text = text.replace("%", " ")
    text = text.replace("*", " ")
    text = text.replace("^", " ")
    text = text.replace("@", " ")
    text = text.replace("&", " ")
    text = text.replace("+", " ")
    text = text.replace("=", " ")
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = text.replace("`", " ")
    text = text.replace("~", " ")
    text = text.replace("،", " ")
    text = text.replace(",", " ")
    text = text.replace(","," ")
    text = text.replace(":", " ")
    text = text.replace(";", " ")
    text = text.replace(".", " ")
    text = text.replace("/", " ")
    text = text.replace("\\", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace("[", " ")
    text = text.replace("]", " ")
    # " - '
    text = text.replace("\u0022", " ") #quotation mark
    text = text.replace("\u0027", " ") #apostrophe
    return text


def remove_half_space(text: str) -> str:
    text = text.replace("\u200c", " ")
    text = text.replace("\u200d", " ")
    return text


def english_numerics_to_persian(text: str) -> str:
    for en, per in zip(ENGLISH_NUMERICS, PERSIAN_NUMERICS):
        text = text.replace(en, per)
    return text


def arabic_to_persian_letters(text: str) -> str:
    # ک عربی
    text = text.replace("\u0643", "\u06a9")
    # ی عربی
    text = text.replace("\u064a", "\u06cc")
    # تشدید
    text = text.replace("\u0651", "")
    #ۀ
    text = text.replace("\u06C0", "") #arabic letter HEH
    text = text.replace("\u0621", "") #arabic letter HAMZAH

    text = text.replace("آ", "ا")
    text = text.replace(" ی ", " ی ")
    #ئ
    text = text.replace("ئ", "ئ")

    return text

def remove_multiple_space(text: str) -> str:
    text = ' '.join(text.split())
    return text

def space_between_alphabets_and_numbers(text: str) -> str:
    result: str = ''
    for i in range(len(text)):
        if text[i].isdigit() and result and result[-1].isalpha():
            result += ' '
        elif text[i].isalpha() and result and result[-1].isdigit():
            result += ' '
        result += text[i]
    return text

def correct_spacing(text: str) -> str:
    for prefix in [
        "می",
        "نمی",

    ]:
        text = text.replace(
            " " + prefix + " ",
            " " + prefix + "\u200c"
        )


    for postfix in [
        "گری",
        "گر",
        "ام",
        "ات",
        "اش",
        "تر",
        "تری",
        "ترین",
        "ها",
        "های",
        "هایی",
        "ای",
    ]:
        text = text.replace(
            " " + postfix + " ",
            "\u200c" + "تر" + " " 
        )
    return text

def two_writing_forms(text: str) -> str:
    two_forms = [ #first is not good, second is good
        ("آزوقه", "آذوقه"),
        ("اطاق", "اتاق"),
        ("اطو", "اطو"),
        ("اصطبل", "اسطبل"),
        ("امپراطور", "امپراتور"),
        ("اطراق", "اتراق"),
        ("باطری", "باتری"),
        ("بلغور", "بلقور"),
        ("تاق", "طاق"),
        ("طپانچه", "تپانچه"),
        ("ذغال", "زغال"),
        ("سوقات", "سوغات"),
        ("غلیان", "قلیان"),
        ("قوتی", "قوطی"),
        ("ملات", "ملاط"),
        ("نفط", "نفت"),
        ("یاطاقان", "یاتاقان"),
        ("طهران", "تهران"),
        ("طیسفون", "تیسفون"),
        ("لوط", "لوت"),
    ]
    for wrong, right in two_forms:
        text = text.replace(wrong, right)
    return text


def normalize(text):
    text = process_abbreviations(text)
    text = remove_multiple_space(text)
    text = space_between_alphabets_and_numbers(text)
    text = correct_spacing(text)
    text = remove_tanvin(text)
    text = remove_erab(text)
    text = remove_endline_tab(text)
    text = remove_punctuations(text)
    # text = remove_half_space(text)
    text = arabic_to_persian_letters(text)
    text = english_numerics_to_persian(text)
    text = two_writing_forms(text)
    text = text.strip()
    return text
