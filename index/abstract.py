from abc import ABC


class AbstractIndex(ABC):
    def insert(self, term: str, doc_id: int, position: int) -> None:
        pass

    def retrieve_sorted_phrase_query(self, prepared_query: list[dict]) -> list[int]:
        pass

    def vocabulary(self):
        pass
