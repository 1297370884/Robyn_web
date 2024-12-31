
"""
    定义复杂查询
    处理复杂的数据库查询逻辑，例如多表关联查询、聚合查询、排序、分页等。
    职责：解耦复杂逻辑，方便复用。
"""

from sqlalchemy import select
from apps.market.models import Product
from sqlalchemy.ext.asyncio import AsyncSession

async def get_products_by_category(db: AsyncSession, category: str):
    """
    根据分类查询产品
    """
    query = select(Product).where(Product.category == category)
    result = await db.execute(query)
    return result.scalars().all()
