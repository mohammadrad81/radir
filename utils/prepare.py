import json
import pickle
from index.positional_index import PositionalIndex
from preprocess.stemming import stem
from preprocess.normalization import normalize
from preprocess.useless_words import remove_useless_words, is_stop_word
from index.positional_index import PositionalIndex
import datetime
from preprocess.tokenization import tokenize

def read_data(file_path: str):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


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
        prepared_content = tokenize(content)
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
    start = datetime.datetime.now()
    index = create_index_from_data(data)
    end = datetime.datetime.now()
    print("index creation time: ", end - start)
    store_index(index, dest_file_path)
    return index, data

def show_results(doc_scores: list[tuple[int, float]], data: dict):
    # print("keys: ", data["0"].keys())
    for doc_id, score in doc_scores:
        str_doc_id = str(doc_id)
        print("doc_id: ", doc_id)
        print("title: ", data[str_doc_id]["title"])
        print("url: ", data[str_doc_id]["url"])
        print("score: ", score)
        print("content: \n", data[str_doc_id]["content"])
        print("-" * 30)
        
        # print("content: ", data[str(doc_id)]["content"])