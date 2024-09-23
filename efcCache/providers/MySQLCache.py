import mysql.connector
from typing import Any, Optional
from efcCache.Interface import CacheInterface
import pickle
import time

class MySQLCache(CacheInterface):
    def __init__(self, connection_string: str, table: str = "cache"):
        self.connection_string = connection_string
        self.table = table
        self._init_db()

    def _init_db(self):
        with mysql.connector.connect(**self._parse_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.table} (
                    `key` VARCHAR(255) PRIMARY KEY,
                    `value` LONGBLOB,
                    `expire` BIGINT
                )
            ''')
            conn.commit()

    def _parse_connection_string(self):
        parts = self.connection_string.split('://')
        user_pass, host_port_db = parts[1].split('@')
        user, password = user_pass.split(':')
        host_port, db = host_port_db.split('/')
        host, port = host_port.split(':')
        return {
            'user': user,
            'password': password,
            'host': host,
            'port': int(port),
            'database': db
        }

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> None:
        expire_time = int(time.time() + expire) if expire else None
        serialized_value = pickle.dumps(value)
        
        with mysql.connector.connect(**self._parse_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                INSERT INTO {self.table} (`key`, `value`, `expire`)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                `value` = VALUES(`value`), `expire` = VALUES(`expire`)
            ''', (key, serialized_value, expire_time))
            conn.commit()

    def get(self, key: str) -> Any:
        with mysql.connector.connect(**self._parse_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT `value`, `expire` FROM {self.table}
                WHERE `key` = %s
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
        with mysql.connector.connect(**self._parse_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                SELECT `expire` FROM {self.table}
                WHERE `key` = %s
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
        with mysql.connector.connect(**self._parse_connection_string()) as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                DELETE FROM {self.table}
                WHERE `key` = %s
            ''', (key,))
            conn.commit()