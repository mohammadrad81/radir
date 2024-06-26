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

    # print("Index loaded.")
    while True:
        query = input("Enter query: \n")
        start = datetime.datetime.now()
        # print("start: ", start)
        prepared_query = prepare_string(query)
        doc_scores = index.retrieve(prepared_query)
        show_results(doc_scores, data)
        finish = datetime.datetime.now()
        # print("finish: ", finish)
        # print("run time: ", (finish - start))