import unittest
from efcCache.providers.FileCache import FileCache
from efcCache.Manager import CacheManager
from efcCache.providers.SQLiteCache import SQLiteCache
from efcCache.providers.RedisCache import RedisCache
from efcCache.providers.MySQLCache import MySQLCache
from efcCache.providers.PostgreSQLCache import PostgreSQLCache



class Test缓存(unittest.TestCase):

    def test_文件缓存(self):
        local_storage = FileCache("./storage/")
        manager = CacheManager(default_storage="local")
        manager.set_storage("local", local_storage)
        
        # 测试设置和获取缓存
        manager.set("key", "value")
        self.assertEqual(manager.get("key"), "value")
        
        # 测试缓存是否存在
        self.assertTrue(manager.exists("key"))
        
        # 测试删除缓存
        manager.delete("key")
        self.assertFalse(manager.exists("key"))
        
        # 测试过期时间
        manager.set("expire_test", "过期测试", expire=1)
        self.assertEqual(manager.get("expire_test"), "过期测试")
        import time
        time.sleep(2)
        self.assertIsNone(manager.get("expire_test"))
        
        # 测试不存在的键
        self.assertIsNone(manager.get("不存在的键"))

    def test_sqlite缓存(self):
        storage = SQLiteCache("./storage/sqlite.db")
        manager = CacheManager(default_storage="sqlite")
        manager.set_storage("sqlite", storage)
        
        # 测试设置和获取缓存
        manager.set("key", "value")
        self.assertEqual(manager.get("key"), "value")
        
        # 测试缓存是否存在
        self.assertTrue(manager.exists("key"))
        
        # 测试删除缓存
        manager.delete("key")
        self.assertFalse(manager.exists("key"))
        
        # 测试过期时间
        manager.set("expire_test", "过期测试", expire=1)
        self.assertEqual(manager.get("expire_test"), "过期测试")
        import time
        time.sleep(2)
        self.assertIsNone(manager.get("expire_test"))
        
        # 测试不存在的键
        self.assertIsNone(manager.get("不存在的键"))
        
    def test_redis缓存(self):
        storage = RedisCache("localhost", 6379, 0)
        manager = CacheManager(default_storage="redis")
        manager.set_storage("redis", storage)
        
        # 测试设置和获取缓存
        manager.set("key", "value")
        self.assertEqual(manager.get("key"), "value")
        
        # 测试缓存是否存在
        self.assertTrue(manager.exists("key"))
        
        # 测试删除缓存
        manager.delete("key")
        self.assertFalse(manager.exists("key"))
        
        # 测试过期时间
        manager.set("expire_test", "过期测试", expire=1)
        self.assertEqual(manager.get("expire_test"), "过期测试")
        import time
        time.sleep(2)
        self.assertIsNone(manager.get("expire_test"))
        
        # 测试不存在的键
        self.assertIsNone(manager.get("不存在的键"))

    def test_mysql缓存(self):
        storage = MySQLCache("mysql://root:@localhost:3306/test")
        manager = CacheManager(default_storage="mysql")
        manager.set_storage("mysql", storage)
        
        # 测试设置和获取缓存
        manager.set("key", "value")
        self.assertEqual(manager.get("key"), "value")
        
        # 测试缓存是否存在
        self.assertTrue(manager.exists("key"))
        
        # 测试删除缓存
        manager.delete("key")
        self.assertFalse(manager.exists("key"))
        
        # 测试过期时间
        manager.set("expire_test", "过期测试", expire=1)
        self.assertEqual(manager.get("expire_test"), "过期测试")
        import time
        time.sleep(2)
        self.assertIsNone(manager.get("expire_test"))
        
        # 测试不存在的键
        self.assertIsNone(manager.get("不存在的键"))

    def test_postgresql缓存(self):
        storage = PostgreSQLCache("postgresql://postgres:@localhost:5432/test")
        manager = CacheManager(default_storage="postgresql")
        manager.set_storage("postgresql", storage)
        
        # 测试设置和获取缓存
        manager.set("key", "value")
        self.assertEqual(manager.get("key"), "value")
        
        # 测试缓存是否存在
        self.assertTrue(manager.exists("key"))
        
        # 测试删除缓存
        manager.delete("key")
        self.assertFalse(manager.exists("key"))
        
        # 测试过期时间
        manager.set("expire_test", "过期测试", expire=1)
        self.assertEqual(manager.get("expire_test"), "过期测试")
        import time
        time.sleep(2)
        self.assertIsNone(manager.get("expire_test"))
        
        # 测试不存在的键
        self.assertIsNone(manager.get("不存在的键"))