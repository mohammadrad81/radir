from .abstract import AbstractIndex
from .posting import PositionalPosting, PositionalPostingList
from utils.query_optimize import smart_intersect
from math import log2

class PositionalIndex(AbstractIndex):
    def __init__(self,
                 postings_list: dict[str, PositionalPostingList] = None,
                 vector_length: dict[int, float]=None):
        self.postings_list = postings_list
        self.vector_length = vector_length
        if self.postings_list is None:
            self.postings_list = dict()


    def insert(self, term: str, doc_id: int, position: int) -> None:
        if term in self.postings_list.keys():
            self.postings_list[term].insert(doc_id, position)
        else:
            posting = PositionalPosting({position})
            self.postings_list[term] = PositionalPostingList({doc_id: posting})

    def vocabulary(self) -> set[str]:
        return set(self.postings_list.keys())

    def doc_vector_length(self) ->dict[int, float]:
        vector_length_squared = dict()
        for term in self.postings_list.keys():
            posting_list = self.postings_list[term]
            for doc_id in posting_list.postings.keys():
                posting = posting_list.postings[doc_id]
                vector_length_squared[doc_id] = vector_length_squared.get(doc_id, 0) + (1 + log2(posting.occurrence)) ** 2
        vector_length = {
            doc_id: vector_length_squared[doc_id]**0.5 
            for doc_id in vector_length_squared
        }
        self.vector_length = vector_length
        return vector_length
    
    def delete_most_frequent_terms(self, k: int) -> list[dict]:
        sorted_terms_by_document_frequency = sorted(self.postings_list.keys(), reverse=True, key=lambda x: self.postings_list[x].document_frequency())
        to_delete = sorted_terms_by_document_frequency[:min(k, len(sorted_terms_by_document_frequency))]
        to_delete_with_document_frequency = [
            {
                "term": t,
                "document_frequency": self.postings_list[t].document_frequency(),
                "collection_frequency": self.postings_list[t].collection_frequency
            }
            for t in to_delete
        ]
        for term in to_delete:
            del self.postings_list[term]
        return to_delete_with_document_frequency

    def retrieve(self, prepared_query: list[dict]) -> list[tuple[int, float]]:
        prepared_query = [d for d in prepared_query if d["term"] in self.postings_list.keys()]
        doc_ids = self.retrieve_absolute_doc_ids(prepared_query)
        sorted_results = self.sorted_results(doc_ids, prepared_query)
        return sorted_results

    def retrieve_absolute_doc_ids(self, prepared_query: list[dict]) -> list[int]:
        # print("prepared query: ", prepared_query)
        result = []
        query_terms_postings_list_doc_ids = [
            set(self.postings_list[d["term"]].postings.keys())
            for d in prepared_query
        ]
        intersected_doc_ids = smart_intersect(query_terms_postings_list_doc_ids)
        if len(intersected_doc_ids) == 0:
            return []
        first_term = prepared_query[0]["term"]
        first_term_position = prepared_query[0]["position"]
        first_term_posting_list = self.postings_list[first_term]
        # print("first_term: ", first_term)
        # print("first_term_position: ", first_term_position)
        for doc_id in intersected_doc_ids:
            # print("doc_id: ", doc_id)
            for first_term_position_in_doc in first_term_posting_list.postings[doc_id].positions:
                is_ok = True
                # print("first_term_position_in_doc: ", first_term_position_in_doc)
                for d in prepared_query[1:]:
                    query_term = d["term"]
                    # print("query_term: ", query_term)
                    query_term_position = d["position"]
                    # print("query_term_position: ", query_term_position)
                    query_term_posting_list = self.postings_list[query_term]
                    position_difference = query_term_position - first_term_position
                    # print("position_difference: ", position_difference)
                    query_term_required_position_in_doc = first_term_position_in_doc + position_difference
                    # print("query_term_required_position_in_doc: ", query_term_required_position_in_doc)
                    is_ok = is_ok and query_term_required_position_in_doc in query_term_posting_list.postings[doc_id].positions
                if is_ok:
                    result.append(doc_id)
                    break
        print("result: ", result)
        return result

    def sorted_results(self, doc_ids: list[int], prepared_query: list[dict]) -> list[tuple[int, float]]:
        query_vector = self.query_vector(prepared_query)
        doc_scores =[
            (doc_id, self.score(doc_id, query_vector))
            for doc_id in doc_ids
        ]
        return sorted(doc_scores, key=lambda x: x[1], reverse=True)
    
    def query_vector(self, prepared_query: list[dict]) -> dict[str, float]:
        query_vector = dict()
        for d in prepared_query:
            term = d["term"]
            query_vector[term] = query_vector.get(term, 0) + 1
        for term in query_vector.keys():
            query_vector[term] = 1 + log2(query_vector[term])
            inverse_document_frequency = log2(len(self.vector_length.keys())/self.postings_list.get(term).document_frequency())
            query_vector[term] *= inverse_document_frequency
        vector_length = 0
        for term in query_vector.keys():
            vector_length += query_vector[term] ** 2
        vector_length == vector_length ** 0.5
        for term in query_vector.keys():
            query_vector[term] /= vector_length
        return query_vector

    def score(self, doc_id: int, query_vector: dict[str, float]) -> float:
        similarity = 0.0
        for term in query_vector:
            term_posting_list = self.postings_list[term]
            document_postings = term_posting_list.postings.get(doc_id, None)
            if document_postings:
                document_term_frequency = 1 + log2(document_postings.occurrence)
                normalized_tf = document_term_frequency / self.vector_length[doc_id]
                similarity += query_vector[term] * normalized_tf
        return similarity
                
    def to_dict(self):
        return {
                    "postings_list":{
                                        x: self.postings_list[x].to_dict()
                                        for x in self.postings_list.keys()
                                    }
                }