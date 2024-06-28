from .abstract import AbstractIndex
from .posting import PositionalPosting, PositionalPostingList
from utils.query_optimize import smart_intersect
from math import log2

class PositionalIndex(AbstractIndex):
    def __init__(self,
                 postings_list: dict[str, PositionalPostingList] = None,
                 vector_length: dict[int, float]=None,
                 documents_doc_ids: set[int] = set()):
        self.postings_list = postings_list
        self.vector_length = vector_length
        self.documents_doc_ids = documents_doc_ids
        if self.postings_list is None:
            self.postings_list = dict()


    def insert(self, term: str, doc_id: int, position: int) -> None:
        if doc_id not in self.documents_doc_ids:
            self.documents_doc_ids.add(doc_id)
        if term in self.postings_list.keys():
            self.postings_list[term].insert(doc_id, position)
        else:
            posting = PositionalPosting({position})
            self.postings_list[term] = PositionalPostingList({doc_id: posting})

    def vocabulary(self) -> set[str]:
        return set(self.postings_list.keys())
    
    def unnormalized_importance_of_term_in_doc(self, term: str, doc_id: int) -> float:
        term_posting_list = self.postings_list.get(term)
        if term_posting_list is None:
            return 0
        posting = term_posting_list.postings[doc_id]
        total_documents_count = len(self.documents_doc_ids)
        term_document_frequency = term_posting_list.document_frequency()
        term_occurrence_in_document = posting.occurrence
        return (1 + log2(term_occurrence_in_document)) * log2(total_documents_count / term_document_frequency)
    
    def normalized_importance_of_term_in_doc(self, term: str, doc_id: int):
        return self.unnormalized_importance_of_term_in_doc(term, doc_id) / self.vector_length[doc_id]

    def doc_vector_length(self) ->dict[int, float]:
        vector_length_squared = dict()
        for term in self.postings_list.keys():
            posting_list = self.postings_list[term]
            for doc_id in posting_list.postings.keys():
                vector_length_squared[doc_id] = vector_length_squared.get(doc_id, 0) + self.unnormalized_importance_of_term_in_doc(term, doc_id) ** 2
        vector_length = {
            doc_id: vector_length_squared[doc_id]**0.5 
            for doc_id in vector_length_squared
        }
        self.vector_length = vector_length
        return vector_length

    def create_champions(self, champions_max_length: int):
        for term in self.postings_list.keys():
            posting_list = self.postings_list[term]
            term_doc_ids = posting_list.postings.keys()
            sorted_term_doc_ids = sorted(term_doc_ids, key=lambda doc_id: self.normalized_importance_of_term_in_doc(term, doc_id), reverse=True)
            champions = sorted_term_doc_ids[:min(len(sorted_term_doc_ids), champions_max_length)]
            posting_list.champions = champions

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

    def retrieve_sorted_phrase_query(self, prepared_query: list[dict]) -> list[tuple[int, float]]:
        prepared_query = [d for d in prepared_query if d["term"] in self.postings_list.keys()]
        doc_ids = self.retrieve_phrase_query(prepared_query)
        sorted_results = self.sorted_results(doc_ids, prepared_query)
        return sorted_results
    
    def retrieve_sorted_non_phrase_query(self, prepared_query: list[dict], count: int = None, champions_only: bool=False) -> list[tuple[int, float]]:
        doc_scores = dict()
        query_vector = self.query_vector(prepared_query)
        for term in query_vector.keys():
            term_score = query_vector[term]
            posting_list = self.postings_list.get(term, None)
            if posting_list is not None:
                if champions_only:
                    for doc_id in posting_list.champions:
                        doc_scores[doc_id] = doc_scores.get(doc_id, 0) + term_score * self.normalized_importance_of_term_in_doc(term, doc_id)
                else:
                    for doc_id in posting_list.postings.keys():
                        doc_scores[doc_id] = doc_scores.get(doc_id, 0) + term_score * self.normalized_importance_of_term_in_doc(term, doc_id)
        doc_scores_list = [(document_id, doc_scores[document_id]) for document_id in doc_scores.keys()]
        sorted_doc_scores_list = sorted(doc_scores_list, reverse=True, key=lambda x: x[1])
        if count is not None:
            sorted_doc_scores_list = sorted_doc_scores_list[:min(count, len(sorted_doc_scores_list))]
        return sorted_doc_scores_list

    def retrieve_phrase_query(self, prepared_query: list[dict]) -> list[int]:
        # print("prepared query: ", prepared_query)
        result = []
        query_terms_postings_list_doc_ids = [
            set(self.postings_list[d["term"]].postings.keys())
            for d in prepared_query
        ]
        intersected_doc_ids = smart_intersect(query_terms_postings_list_doc_ids)
        if len(intersected_doc_ids) == 0:
            return []
        first_term_index = 0
        for i in range(len(prepared_query)):
            first_term = prepared_query[first_term_index]["term"]
            first_term_position = prepared_query[first_term_index]["position"]
            first_term_posting_list = self.postings_list.get(first_term, None)
            if i == len(prepared_query) - 1 and first_term_posting_list is None:
                return []
            elif first_term_posting_list is not None:
                break
        for doc_id in intersected_doc_ids:
            for first_term_position_in_doc in first_term_posting_list.postings[doc_id].positions:
                is_ok = True
                for d in prepared_query[first_term_index + 1:]:
                    query_term = d["term"]
                    query_term_position = d["position"]
                    query_term_posting_list = self.postings_list[query_term]
                    position_difference = query_term_position - first_term_position
                    query_term_required_position_in_doc = first_term_position_in_doc + position_difference
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
        query_vector_length = 0
        for term in query_vector.keys():
            query_vector_length += query_vector[term] ** 2
        query_vector_length == query_vector_length ** 0.5
        for term in query_vector.keys():
            query_vector[term] /= query_vector_length
        return query_vector

    def score(self, doc_id: int, query_vector: dict[str, float]) -> float:
        similarity = 0.0
        for term in query_vector:
            term_posting_list = self.postings_list[term]
            document_postings = term_posting_list.postings.get(doc_id, None)
            if document_postings:
                normalized_doc_score = self.normalized_importance_of_term_in_doc(term, doc_id)
                similarity += query_vector[term] * normalized_doc_score
        return similarity
                
    def to_dict(self):
        return {
                    "postings_list":{
                                        x: self.postings_list[x].to_dict()
                                        for x in self.postings_list.keys()
                                    }
                }