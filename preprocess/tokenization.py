from preprocess.normalization import normalize
from preprocess.stemming import stem
from preprocess.useless_words import is_stop_word

def tokenize(content: str)->list[dict]:
    # print(f"content: \n{content}")
    content = normalize(content)
    tokens = content.split(" ")
    normalized_tokens = [normalize(token) for token in tokens]
    terms = [stem(token) for token in normalized_tokens]
    token_term_position_dicts = [{"position": position, "token": token, "term": term}
                                 for position, (token, term) in enumerate(zip(tokens, terms)) 
                                 if term != "" and not is_stop_word(token)]
    return token_term_position_dicts