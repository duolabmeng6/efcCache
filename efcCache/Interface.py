from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Optional


class CacheInterface(ABC):
    @abstractmethod
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        pass
    
    @abstractmethod
    def get(self, key: str) -> Any:
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        pass