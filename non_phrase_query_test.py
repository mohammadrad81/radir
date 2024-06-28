import json
from index.positional_index import PositionalIndex
from utils.prepare import create_index, load_index, read_data
from utils.prepare import show_results
from preprocess.tokenization import tokenize
import datetime

if __name__ == "__main__":

    # index, data = create_index("IR_data_news_12k.json", "positional_index.pkl")
    with open("IR_data_news_12k.json", "r") as f:
        data = json.load(f)
    index = load_index(index_file_path="positional_index.pkl")
    index.doc_vector_length()
    index.create_champions(100)

    print("Index loaded.")
    for query in [
        "ایران",
        "فوتبال ایران",
        "کریسمس",
        "هدیه کریسمس گواردیولا",

    ]:
        start = datetime.datetime.now()
        # print("start: ", start)
        prepared_query = tokenize(query)
        doc_scores = index.retrieve_sorted_non_phrase_query(prepared_query, champions_only=True, count=3)
        show_results(doc_scores, data, query)
        finish = datetime.datetime.now()
        # print("finish: ", finish)
        # print("run time: ", (finish - start))