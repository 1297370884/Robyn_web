from robyn import Request
from apps.market.api import (
    get_products_api,
    create_product_api,
    get_product_by_id_api,
    get_product_by_name_api,
    update_product_api,
    delete_product_api
)

def market_api_routes(app):
    """
    注册商城路由
    API 路由 - 用于后端接口
    路由层 应该专注于 处理请求 并 返回响应
    """
    @app.get("/api/products")
    async def products_get(request: Request):
        """
        获取所有产品
        """
        return await get_products_api(request)
    
    @app.post("/api/products")
    async def products_create(request: Request):
        """
        创建产品
        """
        return await create_product_api(request)
    
    @app.get("/api/products/:product_id")
    async def product_get_by_id(request: Request):
        """
        通过ID获取单个产品
        """
        return await get_product_by_id_api(request)
    
    @app.get("/api/products/name/:product_name")
    async def product_get_by_name(request: Request):
        """
        通过名称获取单个产品
        """
        return await get_product_by_name_api(request)
    
    @app.put("/api/products/:product_id")
    async def product_update(request: Request):
        """
        更新产品
        """
        return await update_product_api(request)
    
    @app.delete("/api/products/:product_id")
    async def product_delete(request: Request):
        """
        删除产品
        """
        return await delete_product_api(request)