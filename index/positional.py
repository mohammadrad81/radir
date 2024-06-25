from .abstract import AbstractIndex
from .posting import PositionalPosting, PositionalPostingList


class PositionalIndex(AbstractIndex):
    def __init__(self,
                 postings_list: dict[str, PositionalPostingList] = None,
                 ):
        self.postings_list = postings_list

    def insert(self, term: str, doc_id: int, position: int) -> None:
        if term in self.postings_list.keys():
            self.postings_list[term].insert(doc_id, position)
        else:
            posting = PositionalPosting(doc_id, [position])
            self.postings_list[term] = PositionalPostingList([posting])

    def vocabulary(self) -> set[str]:
        return set(self.postings_list.keys())

    def retrieve(self, terms: list[str]) -> list[int]:
        pass

    def to_dict(self):
        return {
                    "postings_list":{
                                        x: self.postings_list[x].to_dict()
                                        for x in self.postings_list.keys()
                                    }
                }