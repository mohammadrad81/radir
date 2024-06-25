import json
import pickle
from index.positional import PositionalIndex
from preprocess.stemming import stem
from preprocess.normalization import normalize
from preprocess.stop_words import remove_stop_words, is_stop_word
from index.positional import PositionalIndex

def read_data(file_path: str):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def prepare_string(content: str)->list[dict]:
    # print(f"content: \n{content}")
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
    token_term_position_dicts = [{"position": position, "token": token, "term": term} for position, (token, term) in enumerate(zip(tokens, terms)) if not is_stop_word(token)]
    return token_term_position_dicts


def create_index_from_data(data: dict) -> PositionalIndex:
    doc_ids = data.keys()
    doc_ids = [int(doc_id) for doc_id in doc_ids]
    doc_ids = sorted(doc_ids)
    # print("number of documents: ", len(doc_ids))
    index = PositionalIndex()
    for i, doc_id in enumerate(doc_ids):
        # if i % 100 == 0:
            # print("inserting doc: ", i, " with id: ", doc_id)
        content = data[str(doc_id)]["content"]
        prepared_content = prepare_string(content)
        for d in prepared_content:
            index.insert(d["term"], doc_id, d["position"])
    return index

def store_index(index: PositionalIndex, index_file_path: str):
    with open(index_file_path, "wb") as file:
        pickle.dump(index, file)

def load_index(index_file_path: str) -> PositionalIndex:
    with open(index_file_path, "rb") as file:
        return pickle.load(file)

def create_index(source_file_path: str, dest_file_path: str) -> tuple[PositionalIndex, dict]:
    data = read_data(source_file_path)
    index = create_index_from_data(data)
    store_index(index, dest_file_path)
    return index, data

def show_results(doc_scores: list[tuple[int, float]], data: dict):
    for doc_id, score in doc_scores:
        print("doc_id: ", doc_id)
        print("score: ", score)
        # print("content: ", data[str(doc_id)]["content"])