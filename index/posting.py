class PositionalPosting:
    def __init__(self,
                 positions: set[int]):
        self.positions = positions

    @property
    def occurrence(self) -> int:
        return len(self.positions)

    def insert(self, new_position: int):
        self.positions.add(new_position)

    def to_dict(self) -> dict:
        return {"positions": sorted(self.positions)}


class PositionalPostingList:
    def __init__(self,
                 postings: dict[int, PositionalPosting]):
        self.postings = postings
        self._collection_frequency = None

    def insert(self, doc_id: int, position: int):

        #if we have the doc already
        if doc_id in self.postings.keys():
            self.postings[doc_id].insert(position)

        #if the doc is new for postings list
        else:
            posting = PositionalPosting({position})
            self.postings[doc_id] = posting

    def document_frequency(self) -> int:
        return len(self.postings)
    
    def recalculate_collection_frequency(self):
        self._collection_frequency = 0
        for posting in self.postings:
            self._collection_frequency += posting.occurrence

    @property
    def collection_frequency(self) -> int:
        if self._collection_frequency is None:
            self.recalculate_collection_frequency()
        return self._collection_frequency

    def to_dict(self) -> dict:
        return {"postings": {
                    "doc_id": doc_id,
                    "posting": self.postings[doc_id].to_dict()
                    }
                    for doc_id in self.postings.keys()
                }