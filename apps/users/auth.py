from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
# from apps.users.utils import send_email, generate_verification_code

""" 验证层 """

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 用于验证输入密码与数据库内加密密码是否一致
def verify_password(plain_password, hashed_password):
    """
    验证密码
    :param plain_password: 输入密码
    :param hashed_password: 数据库内加密密码
    :return: 是否一致
    """
    return pwd_context.verify(plain_password, hashed_password)

# 用于将输入密码加密
def get_password_hash(password):
    """
    获取密码哈希
    :param password: 输入密码
    :return: 加密密码
    """
    return pwd_context.hash(password)

# 算法
ALGORITHM = "HS256"
# 密钥
SECRET_KEY = "your_secret_key"

# 创建访问令牌
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    创建访问令牌
    :param data: 数据
    :param expires_delta: 过期时间
    :return: 访问令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 解码访问令牌
def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# 邮箱验证
def verify_email(email: str):
    return send_email(email, "验证码", generate_verification_code())



