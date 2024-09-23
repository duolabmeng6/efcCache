import unittest
from efcCache.providers.FileCache import FileCache
from efcCache.Manager import CacheManager

class Test文件缓存(unittest.TestCase):

    def test_文件缓存(self):
        local_storage = FileCache("./storage/")
        manager = CacheManager(default_storage="local")
        manager.set_storage("local", local_storage)
        
        # 测试设置和获取缓存
        manager.set("example.txt", "这是一个测试文件")
        self.assertEqual(manager.get("example.txt"), "这是一个测试文件")
        
        # 测试缓存是否存在
        self.assertTrue(manager.exists("example.txt"))
        
        # 测试删除缓存
        manager.delete("example.txt")
        self.assertFalse(manager.exists("example.txt"))
        
        # 测试过期时间
        manager.set("expire_test", "过期测试", expire=1)
        self.assertEqual(manager.get("expire_test"), "过期测试")
        import time
        time.sleep(2)
        self.assertIsNone(manager.get("expire_test"))
        
        # 测试不存在的键
        self.assertIsNone(manager.get("不存在的键"))
