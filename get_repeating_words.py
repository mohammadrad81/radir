import json
from preprocess.normalization import normalize

if __name__ == "__main__":
    word_count: dict[str, int] = dict()
    with open("IR_data_news_12k.json", "r") as file:
        data = json.load(file)
        for doc_id in data.keys():
            seen_in_document = set()
            content: str = normalize(data[doc_id]["content"])
            words = content.split()
            for word in words:
                if word not in seen_in_document:
                    word_count[word] = word_count.get(word, 0) + 1
                    seen_in_document.add(word)
    word_count_list = [(word, count) for word, count in word_count.items()]
    sorted_word_count_list = sorted(word_count_list, key=lambda x: x[1], reverse=True)
    most_frequent_words = sorted_word_count_list[:50]
    print("most frequent words:\n")
    for i, (word, count) in enumerate(most_frequent_words):
        print(f"{i+1}- word: '{word}', frequency: {count}")
    print("\n\n")
    print("to use: \n")
    print("[")
    for word, count in most_frequent_words:
        print(f'"{word}"', ",")
    print("]")