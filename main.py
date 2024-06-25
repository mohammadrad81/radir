import json
from preprocess.stemming import stem
from preprocess.normalization import normalize
from preprocess.stop_words import remove_stop_words, is_stop_word
if __name__ == "__main__":
    with open("IR_data_news_12k.json") as f:
        data = json.load(f)
        content = data["0"]["content"]
        print(f"content: \n{content}")
        tokens = content.split(" ")
        normalized_tokens = [normalize(token) for token in tokens]
        terms = [stem(token) for token in normalized_tokens]
        terms = [{"token": token, "term": term, "is_stop_word": is_stop_word(token)} for (token, term) in zip(tokens, terms)]
        for couple in terms:
            print(couple)