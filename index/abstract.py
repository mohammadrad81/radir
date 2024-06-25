from abc import ABC


class AbstractIndex(ABC):
    def insert(self, term: str, doc_id: int, position: int) -> None:
        pass

    def retrieve(self, terms: list[str]) -> list[int]:
        pass

    def vocabulary(self):
        pass
