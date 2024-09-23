from typing import Any, List, Optional

from .Interface import CacheInterface


# 缓存管理器
class CacheManager:
    def __init__(self, default_storage: str = "file"):
        self.storages = {}
        self.default_storage = default_storage
    
    def set_storage(self, name: str, storage: CacheInterface) -> None:
        self.storages[name] = storage
    
    def get_storage(self, name: str) -> CacheInterface:
        return self.storages.get(name)
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        self.storages[self.default_storage].set(key, value, expire)
    
    def get(self, key: str) -> Any:
        return self.storages[self.default_storage].get(key)
    
    def exists(self, key: str) -> bool:
        return self.storages[self.default_storage].exists(key)
    
    def delete(self, key: str) -> None:
        self.storages[self.default_storage].delete(key)