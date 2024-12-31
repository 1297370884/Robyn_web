from robyn import Robyn, Request
from apps.users.views.views import (
    login_user_view,
    logout_user_view
)

def users_view_routes(app):
    """
    用户视图 路由 
    路由层 应该专注于 处理请求 并 返回响应
    """
    
    app.add_route(route_type="POST", endpoint="/users/login", handler=login_user_view) # 登录路由
    app.add_route(route_type="GET", endpoint="/users/logout", handler=logout_user_view) # 登出路由
