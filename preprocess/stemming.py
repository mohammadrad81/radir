#hazm stemmer
#I was not able to install hazm

REMOVING_ENDS = [
    "ات",
    "ان",
    "ترین",
    "تر",
    "م",
    "ت",
    "ش",
    "یی",
    "ی",
    "ها",
    "ٔ",
    "‌ا",
    "‌",
]

def stem(word: str, removing_ends: list[str] = None) -> str:
    if removing_ends is None:
        removing_ends = REMOVING_ENDS
    for end in removing_ends:
        if word.endswith(end) and len(word) > len(end): #improvement
            word = word[:-len(end)]

    if word.endswith("ۀ"):
        word = word[:-1] + "ه"

    return word
