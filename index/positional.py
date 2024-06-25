from .abstract import AbstractIndex
from .posting import PositionalPosting, PositionalPostingList


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
                vector_length_squared[doc_id] = vector_length_squared.get(doc_id, 0) + posting.occurrence ** 2
        vector_length = {
            doc_id: vector_length_squared[doc_id]**0.5 
            for doc_id in vector_length_squared
        }
        self.vector_length = vector_length
        return vector_length

    def retrieve(self, terms: list[str]) -> list[int]:
        pass

    def to_dict(self):
        return {
                    "postings_list":{
                                        x: self.postings_list[x].to_dict()
                                        for x in self.postings_list.keys()
                                    }
                }