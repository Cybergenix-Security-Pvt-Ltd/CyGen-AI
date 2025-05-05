from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def check_trigger(self) -> bool:
        raise NotImplementedError
