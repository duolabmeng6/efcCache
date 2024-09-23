import sqlite3
from typing import Any, Optional
from efcCache.Interface import CacheInterface
import pickle
import time

class SQLiteCache(CacheInterface):
    def __init__(self, storage_path: str, table: str = "cache"):
        self.storage_path = storage_path
        self.table = table
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.storage_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table} (
                    key TEXT PRIMARY KEY,
                    value BLOB,
                    expire INTEGER
                )
            ''')
            conn.commit()

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        expire_time = int(time.time() + expire) if expire else None
        serialized_value = pickle.dumps(value)
        
        with sqlite3.connect(self.storage_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                INSERT OR REPLACE INTO {self.table} (key, value, expire)
                VALUES (?, ?, ?)
            ''', (key, serialized_value, expire_time))
            conn.commit()

    def get(self, key: str) -> Any:
        with sqlite3.connect(self.storage_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT value, expire FROM {self.table}
                WHERE key = ?
            ''', (key,))
            result = cursor.fetchone()

        if result:
            value, expire = result
            if expire is None or expire > int(time.time()):
                return pickle.loads(value)
            else:
                self.delete(key)
        return None

    def exists(self, key: str) -> bool:
        with sqlite3.connect(self.storage_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT expire FROM {self.table}
                WHERE key = ?
            ''', (key,))
            result = cursor.fetchone()

        if result:
            expire = result[0]
            if expire is None or expire > int(time.time()):
                return True
            else:
                self.delete(key)
        return False

    def delete(self, key: str) -> None:
        with sqlite3.connect(self.storage_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                DELETE FROM {self.table}
                WHERE key = ?
            ''', (key,))
            conn.commit()