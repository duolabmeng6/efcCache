import redis
from typing import Any, Optional
from efcCache.Interface import CacheInterface
import pickle

class RedisCache(CacheInterface):
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0, **kwargs):
        self.client = redis.Redis(host=host, port=port, db=db, **kwargs)

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        serialized_value = pickle.dumps(value)
        if expire:
            self.client.setex(key, expire, serialized_value)
        else:
            self.client.set(key, serialized_value)

    def get(self, key: str) -> Any:
        value = self.client.get(key)
        if value:
            return pickle.loads(value)
        return None

    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0

    def delete(self, key: str) -> None:
        self.client.delete(key)