class PositionalPosting:
    def __init__(self,
                 doc_id: int,
                 positions: list[int]):
        self.doc_id = doc_id
        self.positions = positions

    @property
    def occurrence(self) -> int:
        return len(self.positions)

    def append(self, new_position: int):
        self.positions.append(new_position)

    def to_dict(self) -> dict:
        return {"doc_id": self.doc_id,
                "positions": self.positions}


class PositionalPostingList:
    def __init__(self,
                 postings: list[PositionalPosting]):
        self.postings = postings
        self._collection_frequency = None

    def insert(self, doc_id: int, position: int):

        #if we have the doc already
        for posting in self.postings:
            if posting.doc_id == doc_id:
                posting.append(position)
                return

        #if the doc is new for postings list
        posting = PositionalPosting(doc_id, [position])
        self.postings.append(posting)

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
        return {"postings": [p.to_dict() for p in self.postings]}