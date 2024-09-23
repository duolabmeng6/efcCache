import psycopg2
from typing import Any, Optional
from efcCache.Interface import CacheInterface
import pickle
import time

class PostgreSQLCache(CacheInterface):
    def __init__(self, connection_string: str, table: str = "cache"):
        self.connection_string = connection_string
        self.table = table
        self._init_db()

    def _init_db(self):
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {self.table} (
                        key TEXT PRIMARY KEY,
                        value BYTEA,
                        expire BIGINT
                    )
                ''')
            conn.commit()

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        expire_time = int(time.time() + expire) if expire else None
        serialized_value = pickle.dumps(value)
        
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''
                    INSERT INTO {self.table} (key, value, expire)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (key) DO UPDATE
                    SET value = EXCLUDED.value, expire = EXCLUDED.expire
                ''', (key, psycopg2.Binary(serialized_value), expire_time))
            conn.commit()

    def get(self, key: str) -> Any:
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''
                    SELECT value, expire FROM {self.table}
                    WHERE key = %s
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
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''
                    SELECT expire FROM {self.table}
                    WHERE key = %s
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
        with psycopg2.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'''
                    DELETE FROM {self.table}
                    WHERE key = %s
                ''', (key,))
            conn.commit()