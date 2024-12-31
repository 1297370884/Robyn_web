from robyn import Request
from apps.users.services import (
    login_user,
    logout_user
)

"""
视图层 应该专注于 处理请求 并 返回响应
"""

# async def register_user_view(request: Request):
#     """
#     注册用户视图
#     """
#     return await register_precheck_and_send_verification(request)
    
async def login_user_view(request: Request):  
    """
    登录用户视图
    """
    request_data = request.json()
    account = request_data.get("account")
    password = request_data.get("password")
    return await login_user(account, password)


async def logout_user_view(request: Request):
    """
    登出用户视图
    """
    return await logout_user(request)







