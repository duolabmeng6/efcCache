# efcCache

efcCache 是一个通用的缓存类库,支持多种存储后端,包括:

- 本地文件
- SQLite
- MySQL
- PostgreSQL
- Redis


## 安装

使用 pip 安装 efcCache:

```bash
pip install efcCache
```

## 快速开始

以下是一个使用 efcCache 的简单示例:

```python
import efcCache
from efcCache.providers.FileCache import FileCache
from efcCache.providers.RedisCache import RedisCache
from efcCache.providers.SQLiteCache import SQLiteCache
from efcCache.providers.MySQLCache import MySQLCache
from efcCache.providers.PostgreSQLCache import PostgreSQLCache

# 创建缓存管理器
manager = efcCache.CacheManager(default_storage="local")

# 设置存储后端
manager.set_storage("local", FileCache(storage_path="./storage/"))
manager.set_storage("redis", RedisCache(host="localhost", port=6379, db=0))
manager.set_storage("sqlite", SQLiteCache(storage_path="./storage/sqlite.db"))
manager.set_storage("mysql", MySQLCache(connection_string="mysql://root:password@localhost:3306/test", table="cache"))
manager.set_storage("postgresql", PostgreSQLCache(connection_string="postgresql://postgres:password@localhost:5432/test", table="cache"))

# 使用示例
manager.set("key", "value")
print(manager.get("key"))
print(manager.exists("key"))
manager.delete("key")

# 直接访问特定存储后端
manager.get_storage("redis").get("key")
manager.get_storage("mysql").get("key")

```

## 贡献

欢迎贡献代码、报告问题或提出改进建议。请查看我们的[贡献指南](CONTRIBUTING.md)了解更多信息。

## 许可证

efcCache 使用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。
