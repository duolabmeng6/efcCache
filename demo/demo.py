import efcCache
from efcCache.providers.FileCache import FileCache
from efcCache.providers.SQLiteCache import SQLiteCache
from efcCache.providers.RedisCache import RedisCache
from efcCache.providers.MySQLCache import MySQLCache
from efcCache.providers.PostgreSQLCache import PostgreSQLCache

# 创建缓存管理器
manager = efcCache.CacheManager(default_storage="local")

# 设置存储后端
manager.set_storage("local", FileCache(storage_path="./storage/"))
manager.set_storage("sqlite", SQLiteCache(storage_path="./storage/cache.db"))
manager.set_storage("redis", RedisCache(host="localhost", port=6379, db=0))
manager.set_storage("mysql", MySQLCache(connection_string="mysql://root:password@localhost:3306/test", table="cache"))
manager.set_storage("postgresql", PostgreSQLCache(connection_string="postgresql://postgres:password@localhost:5432/test", table="cache"))

# 测试文件缓存
print("测试文件缓存:")
manager.get_storage("local").set("test", "文件缓存测试")
print(manager.get_storage("local").get("test"))
print(manager.get_storage("local").exists("test"))
manager.get_storage("local").delete("test")
print(manager.get_storage("local").exists("test"))

# 测试SQLite缓存
print("\n测试SQLite缓存:")
manager.get_storage("sqlite").set("test", "SQLite缓存测试")
print(manager.get_storage("sqlite").get("test"))
print(manager.get_storage("sqlite").exists("test"))
manager.get_storage("sqlite").delete("test")
print(manager.get_storage("sqlite").exists("test"))

# 测试Redis缓存
print("\n测试Redis缓存:")
manager.get_storage("redis").set("test", "Redis缓存测试")
print(manager.get_storage("redis").get("test"))
print(manager.get_storage("redis").exists("test"))
manager.get_storage("redis").delete("test")
print(manager.get_storage("redis").exists("test"))

# 测试MySQL缓存
print("\n测试MySQL缓存:")
manager.get_storage("mysql").set("test", "MySQL缓存测试")
print(manager.get_storage("mysql").get("test"))
print(manager.get_storage("mysql").exists("test"))
manager.get_storage("mysql").delete("test")
print(manager.get_storage("mysql").exists("test"))

# 测试PostgreSQL缓存
print("\n测试PostgreSQL缓存:")
manager.get_storage("postgresql").set("test", "PostgreSQL缓存测试")
print(manager.get_storage("postgresql").get("test"))
print(manager.get_storage("postgresql").exists("test"))
manager.get_storage("postgresql").delete("test")
print(manager.get_storage("postgresql").exists("test"))

# 测试过期时间
print("\n测试过期时间:")
manager.get_storage("local").set("expire_test", "过期测试", expire=5)
print(manager.get_storage("local").get("expire_test"))
import time
print("等待6秒...")
time.sleep(6)
print(manager.get_storage("local").get("expire_test"))

# 测试默认存储
print("\n测试默认存储:")
manager.set("default_test", "默认存储测试")
print(manager.get("default_test"))
print(manager.exists("default_test"))
manager.delete("default_test")
print(manager.exists("default_test"))

