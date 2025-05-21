from abc import ABC, abstractmethod

class Base(ABC):
    def __init__(self, query: str) -> None:
        self.query = query

    @abstractmethod
    def check_trigger(self) -> bool:
        raise NotImplementedError
