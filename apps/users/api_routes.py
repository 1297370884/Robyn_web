from robyn import Request
from apps.users.api import (
    create_user_api,
    get_users_api,
    get_user_api,
    update_user_api,
    delete_user_api,
    fuzzy_search_user_api,
    update_user_field_api
)

def users_api_routes(app):
    """
    注册用户路由
    API 路由 - 用于后端接口
    路由层 应该专注于 处理请求 并 返回响应
    """
    @app.get("/api/users")
    async def users_get(request):
        """
        获取所有用户
        """
        return await get_users_api(request)
    
    @app.post("/api/users")
    async def users_create(request):
        """
        创建用户
        """
        return await create_user_api(request)
    
    @app.get("/api/users/:user_id")
    async def user_get(request):
        """
        获取单个用户
        """
        return await get_user_api(request)
    
    @app.put("/api/users/:user_id")
    async def user_update(request):
        """
        更新用户
        """
        return await update_user_api(request)
    
    @app.patch("/api/users/:user_id")
    async def user_update_field(request):
        """
        更新用户指定字段
        """
        return await update_user_field_api(request)
    
    @app.delete("/api/users/:user_id")
    async def user_delete(request):
        """
        删除用户
        """
        return await delete_user_api(request)