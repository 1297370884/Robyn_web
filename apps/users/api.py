from robyn.robyn import Request
from apps.users.services import create_user_service, delete_user_service, fuzzy_search_user, get_user_by_email, get_user_by_id, get_user_by_phone, get_user_by_username, get_users_service, update_user_field_service, update_user_service

"""
    定义用户API接口
    接口层 应该专注于 处理基础的数据库操作 并 返回成功的状态码及数据内容
    接口层避免直接暴露在外,应该由服务层调用
"""

# @app.post("/user")
async def create_user_api(request: Request):
    """
    创建用户
    """
    return await create_user_service(request)

# @app.get("/users")
async def get_users_api(request: Request):
    """
    获取用户列表 接口
    """
    return await get_users_service(request)


# @app.get("/user/:user_id")
async def get_user_api(request: Request):
    """
    通过用户ID获取单个用户 接口
    """
    return await get_user_by_id(request)


# @app.get("/user/username")
async def get_user_by_username_api(request: Request):
    """
    通过用户名获取单个用户 接口
    """
    return await get_user_by_username(request)


# @app.get("/user/email")
async def get_user_by_email_api(request: Request):
    """
    通过邮箱获取单个用户 接口
    """
    return await get_user_by_email(request)


# @app.get("/user/phone")
async def get_user_by_phone_api(request: Request):
    """
    通过手机号获取单个用户 接口
    """
    return await get_user_by_phone(request)
    

async def fuzzy_search_user_api(request: Request):
    """
    账号匹配用户 接口
    """
    return await fuzzy_search_user(request)

    
# @app.put("/user/:user_id")
async def update_user_api(request: Request):
    """
    更新用户
    """
    return await update_user_service(request)


# @app.patch("/user/:user_id")
async def update_user_field_api(request: Request):
    """
    更新用户指定字段
    """
    return await update_user_field_service(request)

# @app.delete("/user/:user_id")
async def delete_user_api(request: Request):
    """
    删除用户
    """
    return await delete_user_service(request)