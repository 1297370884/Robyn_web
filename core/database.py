from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# MariaDB 连接配置
DATABASE_URL = "mysql+aiomysql://lpl:lpllz2233233@localhost/robyn_db"

# 创建异步数据库引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 设置为 True 可以看到 SQL 语句
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 创建异步基类
class Base(DeclarativeBase):
    pass

# 获取异步数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

