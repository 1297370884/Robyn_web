import json
from robyn import Headers, Request, Response, jsonify, status_codes
from apps.users import crud
from apps.users.models import User
from apps.users.auth import get_password_hash, verify_password, create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
# from apps.users.utils import send_email, generate_verification_code
from core.database import AsyncSessionLocal

"""
    crud -> services -> api
    服务层:根据业务逻辑整合crud数据操作 封装业务方法 可以由上层函数直接调用
    服务层 应该完成 业务逻辑（如判断数据是否存在、响应失败的处理逻辑）
"""

# 接口调用
async def get_user_by_id(request):
    """
    通过用户ID获取单个用户
    """
    try:
        async with AsyncSessionLocal() as db:
            user_id = request.path_params.get("user_id")
            user_obj = await crud.get_user(db, user_id) # 获取用户
            if not user_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "User not found"}))

            return Response(status_code=status_codes.HTTP_200_OK,
                            headers={"Content-Type": "application/json"},
                            description=jsonify(user_obj.to_dict()))
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "获取用户失败"}))
    
# 接口调用
async def get_user_by_username(username):
    """
    通过用户名获取单个用户
    """
    try:
        async with AsyncSessionLocal() as db:
            user_obj = await crud.get_user_by_filter(db, {"username": username})
            if not user_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "User not found"}))
            

            return Response(status_code=status_codes.HTTP_200_OK,
                            headers={"Content-Type": "application/json"},
                            description=jsonify(user_obj.to_dict()))
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "获取用户失败"}))


async def get_user_by_email(email):
    """
    通过邮箱获取单个用户
    """
    try:
        async with AsyncSessionLocal() as db:
            user_obj = await crud.get_user_by_filter(db, {"email": email})
            
            if user_obj:
                user_data = {
                    'id': user_obj.id,
                    'username': user_obj.username,
                    'email': user_obj.email,
                    'password': user_obj.password,
                    'phone': user_obj.phone,
                    'address': user_obj.address,
                    'is_active': user_obj.is_active,
                    'is_admin': user_obj.is_admin,
                    'created_at': str(user_obj.created_at),
                    'updated_at': str(user_obj.updated_at),
                    'is_deleted': user_obj.is_deleted
                }
                return Response(
                    status_code=status_codes.HTTP_200_OK,
                    headers={"Content-Type": "application/json"},
                    description=jsonify(user_data)
                )
            return Response(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                headers={"Content-Type": "application/json"},
                description=jsonify({"message": "User not found"})
            )
    except Exception as e:
        print(f"Error: {e}")
        return Response(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
            headers={"Content-Type": "application/json"}, 
            description=jsonify({"message": "获取用户失败"})
        )

async def get_user_by_phone(phone):
    """
    通过手机号获取单个用户
    """
    try:
        async with AsyncSessionLocal() as db:
            user_obj = await crud.get_user_by_filter(db, {"phone": phone})
            if not user_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "User not found"}))
            
            return Response(status_code=status_codes.HTTP_200_OK,
                            headers={"Content-Type": "application/json"},
                            description=jsonify(user_obj.to_dict()))
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "获取用户失败"}))


async def fuzzy_search_user(account):
    """
    账号匹配用户
    """
    try:
        async with AsyncSessionLocal() as db:
            user_obj = await crud.get_user_by_filter(db, {"username": account}) or await crud.get_user_by_filter(db, {"email": account}) or await crud.get_user_by_filter(db, {"phone": account})
            if not user_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "User not found"}))
            
            return Response(status_code=status_codes.HTTP_200_OK,
                            headers={"Content-Type": "application/json"},
                            description=jsonify(user_obj.to_dict()))
        
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "模糊搜索用户失败"}))

# 管理员权限 接口调用
async def get_users_service(request):
    """
    获取所有用户列表
    """
    try:
        async with AsyncSessionLocal() as db:
            users_obj = await crud.get_users_by_filters(db)
            
            users_data = [user.to_dict() for user in users_obj]

            return Response(
                status_code=status_codes.HTTP_200_OK,
                headers={"Content-Type": "application/json"},
                description=jsonify(users_data)
            )
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "获取用户失败"}))

# 管理员权限 接口调用
async def create_user_service(request):
    """
    创建用户接口 管理员权限
    """
    try:
        user_data = request.json()
        username = user_data.get("username")
        email = user_data.get("email")
        phone = user_data.get("phone")
        password = user_data.get("password")
        
        # 确保必填字段都存在
        if not all([username, email, phone, password]):
            return Response(status_code=status_codes.HTTP_400_BAD_REQUEST,
                          headers={"Content-Type": "application/json"},
                          description=jsonify({"message": "Missing required fields"}))

        # 检查用户是否已存在
        async with AsyncSessionLocal() as db:
            user_exists = (await crud.get_user_by_filter(db, {"username": username}) or 
                         await crud.get_user_by_filter(db, {"email": email}) or 
                         await crud.get_user_by_filter(db, {"phone": phone}))
            
            # 如果用户已存在，则返回错误信息
            if user_exists:
                return Response(status_code=status_codes.HTTP_409_CONFLICT,
                            headers={"Content-Type": "application/json"},
                            description=jsonify({"message": "User already exists"}))

            # 如果用户不存在，则创建用户
            user_data["password"] = get_password_hash(user_data["password"])  # 加密密码

            try:
                inserted_user = await crud.create_user(db, user_data) # 创建用户
                if not inserted_user:
                    raise Exception("User creation failed")  # 抛出异常
                return Response(status_code=status_codes.HTTP_200_OK,
                                headers={"Content-Type": "application/json"},
                                description=jsonify(inserted_user.to_dict()))

            except Exception as e:  # 数据库操作的关键异常
                raise Exception(f"Database integrity error: {str(e)}")

    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "创建用户失败"}))


async def update_user_service(request):
    """
    更新用户
    """
    try:
        async with AsyncSessionLocal() as db:
            user_id = request.path_params.get("user_id")
            user_data = request.json()
            user_obj = await crud.get_user(db, user_id)
            if not user_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "User not found"}))
            

            user_data["password"] = get_password_hash(user_data["password"])  # 加密密码
    
            user = await crud.update_user(db, user_id, user_data)
            if not user:
                raise Exception("---->User update failed")
            
            return Response(status_code=status_codes.HTTP_200_OK, 
                            headers={"Content-Type": "application/json"}, 
                            description=jsonify(user.to_dict()))
    except Exception as e:
        print(f"Error: {e}")
        await db.rollback()
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "更新用户失败"}))
    
async def update_user_field_service(request):
    """
    更新用户指定字段
    """
    try:
        async with AsyncSessionLocal() as db:
            user_id = request.path_params.get("user_id")
            user_obj = await crud.get_user(db, user_id)
            if not user_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "User not found"}))
            
            user_data = request.json()

            # 处理布尔值字段
            bool_fields = ['is_admin', 'is_active', 'is_deleted']
            for field in bool_fields:
                if field in user_data:
                    # 处理字符串类型的布尔值
                    if isinstance(user_data[field], str):
                        user_data[field] = user_data[field].lower() == 'true'
                    else:
                        user_data[field] = bool(user_data[field])

            # 如果更新密码，需要加密
            if "password" in user_data:
                user_data["password"] = get_password_hash(user_data["password"])
                
            user = await crud.update_user(db, user_id, user_data)
            if not user:
                raise Exception("---->User update failed")
            
            return Response(status_code=status_codes.HTTP_200_OK, 
                            headers={"Content-Type": "application/json"}, 
                            description=jsonify(user.to_dict()))
    except Exception as e:
        print(f"Error: {e}")
        await db.rollback()
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "更新用户失败"}))

async def delete_user_service(request):
    """
    删除用户
    """
    try:
        async with AsyncSessionLocal() as db:
            user_id = request.path_params.get("user_id")
            user_obj = await crud.get_user(db, user_id)
            if not user_obj:
                return Response(status_code=status_codes.HTTP_404_NOT_FOUND,
                                headers={"Content-Type": "application/json"},
                                description=jsonify({"message": "User not found"}))
            
            user = await crud.delete_user(db, user_id) 
            if not user:
                raise Exception("User delete failed")
            
            return Response(status_code=status_codes.HTTP_200_OK, 
                            headers=Headers({}),
                            description="OK")
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "删除用户失败"}))


# 登录逻辑 验证用户并返回令牌，以维持用户登录状态
async def login_user(account: str, password: str):
    """
    登录用户
    """
    # 获取用户响应
    user_response = await get_user_by_email(account) or await get_user_by_phone(account)
    
    # 检查响应状态码
    if user_response.status_code != status_codes.HTTP_200_OK:
        return Response(
            status_code=status_codes.HTTP_404_NOT_FOUND, 
            headers={"Content-Type": "application/json"}, 
            description=jsonify({"message": "用户不存在"})
        )

    try:
        # 从响应中获取用户数据
        user_data = json.loads(user_response.description)
        if not verify_password(password, user_data["password"]):
            return Response(
                status_code=status_codes.HTTP_401_UNAUTHORIZED, 
                headers={"Content-Type": "application/json"}, 
                description=jsonify({"message": "密码错误"})
            )
        
        # 生成Token
        created_token = create_access_token(data={"sub": user_data["username"]})

        # 创建响应
        response = Response(
            status_code=status_codes.HTTP_200_OK, 
            headers={"Content-Type": "application/json"}, 
            description=jsonify({
                "status": "success",
                "message": "登录成功"
            })
        )
        # 设置HttpOnly Cookie
        response.headers["Set-Cookie"] = (
            f"access_token=Bearer {created_token}; "
            f"HttpOnly; Secure; Path=/; SameSite=Strict"
        )

        return response
    except Exception as e:
        print(f"Error processing user data: {e}")
        return Response(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
            headers={"Content-Type": "application/json"}, 
            description=jsonify({"message": "登录处理失败"})
        )


# 注册逻辑 创建新用户
async def register_precheck_and_send_verification(request):
    """
    注册预校验并发送验证码
    """
    try:
        user_data = request.json()
        username = user_data.get("username")
        email = user_data.get("email")
        phone = user_data.get("phone")
        password = user_data.get("password")
        
        # 确保必填字段都存在
        if not all([username, email, phone, password]):
            return Response(status_code=status_codes.HTTP_400_BAD_REQUEST,
                          headers={"Content-Type": "application/json"},
                          description=jsonify({"message": "Missing required fields"}))

        # 检查用户是否已存在
        async with AsyncSessionLocal() as db:
            user_exists = (await crud.get_user_by_column(db, "username", username) or 
                         await crud.get_user_by_column(db, "email", email) or 
                         await crud.get_user_by_column(db, "phone", phone))
        
        if user_exists:
            return Response(status_code=status_codes.HTTP_409_CONFLICT,
                          headers={"Content-Type": "application/json"},
                          description=jsonify({"message": "User already exists"}))

        # 生成6位数邮箱验证码
        verification_code = generate_verification_code()
        # save_to_cache(email, verification_code, expire=300)  # 有效期5分钟

        # 发送邮箱验证码
        is_send = await send_email(email, "验证码", verification_code)
        if not is_send:
            return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                            headers={"Content-Type": "application/json"}, 
                            description=jsonify({"message": "邮件发送失败"}))
        
        # 发送成功
        return Response(status_code=status_codes.HTTP_200_OK, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "发送成功"}))

    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR, 
                        headers={"Content-Type": "application/json"}, 
                        description=jsonify({"message": "注册失败"}))


# async def verify_code_and_create_user(request):
#     """
#     验证验证码并创建用户
#     """
#     data = await request.json()
#     email = data.get("email")
#     verification_code = data.get("verification_code")

#     # 从缓存中获取验证码
#     cached_code = get_from_cache(email)
#     if not cached_code or cached_code != verification_code:
#         return Response(status_code=status_codes.HTTP_400_BAD_REQUEST, headers={"Content-Type": "application/json"}, description="验证码错误或已过期")

#     # 验证成功后创建用户
#     async with AsyncSessionLocal() as db:
#         user_data = {
#             "username": data.get("username"),
#             "email": email,
#             "phone": data.get("phone"),
#             "password": get_password_hash(data.get("password"))
#         }
#         new_user = User(**user_data)
#         await crud.create_user(db, new_user)

#     # 删除缓存中的验证码
#     delete_from_cache(email)

#     # 创建令牌
#     created_token = create_access_token(data={"sub": user_data.get("username")})

#     return Response(status_code=status_codes.HTTP_200_OK, description="用户注册成功", data={"token": created_token})


# 登出逻辑 清除令牌
async def logout_user(request):
    """
    登出用户，清除 access_token 并返回成功信息
    """
    try:
        # 清除 Cookie 中的 access_token
        response = Response(
            status_code=status_codes.HTTP_200_OK,
            description=json.dumps({"status": "success", "message": "登出成功"}),
            headers={
                "Content-Type": "application/json",
                # 设置 Set-Cookie 响应头以清除 access_token
                "Set-Cookie": "access_token=; Path=/; HttpOnly; Expires=Thu, 01 Jan 1970 00:00:00 GMT;"
            }
        )
        return response
    except Exception as e:
        print(f"Error during logout: {e}")
        return Response(
            status_code=status_codes.HTTP_500_INTERNAL_SERVER_ERROR,
            description=json.dumps({"status": "error", "message": "登出失败"}),
            headers={"Content-Type": "application/json"}
        )
