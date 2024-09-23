import os
import json
import time
from typing import Any, List, Optional

from ..Interface import CacheInterface


class FileCache(CacheInterface):
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
    
    def _get_file_path(self, key: str) -> str:
        return os.path.join(self.storage_path, f"{key}.json")
    
    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        file_path = self._get_file_path(key)
        data = {
            "value": value,
            "expire": time.time() + expire if expire else None
        }
        with open(file_path, "w") as f:
            json.dump(data, f)
    
    def get(self, key: str) -> Any:
        file_path = self._get_file_path(key)
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, "r") as f:
            data = json.load(f)
        
        if data["expire"] and time.time() > data["expire"]:
            os.remove(file_path)
            return None
        
        return data["value"]
    
    def exists(self, key: str) -> bool:
        return os.path.exists(self._get_file_path(key))
    
    def delete(self, key: str) -> None:
        file_path = self._get_file_path(key)
        if os.path.exists(file_path):
            os.remove(file_path)