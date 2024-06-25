import json
from preprocess.stemming import stem
from preprocess.normalization import normalize
from preprocess.stop_words import remove_stop_words, is_stop_word
from index.positional import PositionalIndex
if __name__ == "__main__":
    with open("IR_data_news_12k.json") as f:
        data = json.load(f)
        content = data["0"]["content"]
        print(f"content: \n{content}")
        content = content.replace("\n", " ")
        content = ' '.join(content.split())
        content = content.replace(
            " می ",
            " " + "می" + "\u200c"
        )
        content = content.replace(
            " نمی ",
            " " + "نمی" + "\u200c"
        )
        
        tokens = content.split(" ")
        normalized_tokens = [normalize(token) for token in tokens]
        terms = [stem(token) for token in normalized_tokens]
        terms = [{"position": position, "token": token, "term": term, "is_stop_word": is_stop_word(token)} for position, (token, term) in enumerate(zip(tokens, terms))]
        # for couple in terms:
        #     print(couple)
        index = PositionalIndex()
        for d in terms:
            if not d["is_stop_word"]:
                index.insert(d["term"], 0, d["position"])

        print("index constructed\n\n")
        print(index.to_dict())
        