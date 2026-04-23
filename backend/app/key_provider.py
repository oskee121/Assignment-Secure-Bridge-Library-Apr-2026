from abc import ABC, abstractmethod


class KeyProvider(ABC):
    @abstractmethod
    def get_current_key(self) -> tuple[str, bytes]:
        pass

    @abstractmethod
    def get_key(self, version: str) -> bytes:
        pass
