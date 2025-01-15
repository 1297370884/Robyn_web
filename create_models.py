from core.database import Base, engine
from apps.users.models import User
from apps.market.models import Product


async def init_db():
    async with engine.begin() as conn:
        # 创建表
        await conn.run_sync(Base.metadata.create_all)

import asyncio
asyncio.run(init_db())

# 确保在程序退出时关闭事件循环
loop = asyncio.get_event_loop()
loop.run_until_complete(loop.shutdown_asyncgens())
loop.close()

