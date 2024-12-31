from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class User(Base):
    """
    用户模型，用于定义用户表
    """
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, phone={self.phone}, password={self.password}, address={self.address}, is_active={self.is_active}, is_admin={self.is_admin}, created_at={self.created_at}, updated_at={self.updated_at}, is_deleted={self.is_deleted})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "address": self.address,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_deleted": self.is_deleted
        }


