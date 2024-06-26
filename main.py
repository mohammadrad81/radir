import json
from index.positional import PositionalIndex
from utils.prepare import create_index, load_index, read_data
from utils.prepare import prepare_string, show_results
import datetime

if __name__ == "__main__":

    index, data = create_index("IR_data_news_12k.json", "positional_index.pkl")
    # index = load_index("positional_index.pkl")
    # data = read_data("IR_data_news_12k.json")
    index.doc_vector_length()
    most_frequent_terms: list[dict] = index.delete_most_frequent_terms(50)
    for d in most_frequent_terms:
        print("term: ", d["term"])
        print("document frequency: ", d["document_frequency"])
        print("collection frequency", d["collection_frequency"])

    # print("Index loaded.")
    # while True:
    #     query = input("Enter query: \n")
    #     start = datetime.datetime.now()
        # print("start: ", start)
        # prepared_query = prepare_string(query)
        # doc_scores = index.retrieve(prepared_query)
        # show_results(doc_scores, data)
        # finish = datetime.datetime.now()
        # print("finish: ", finish)
        # print("run time: ", (finish - start))