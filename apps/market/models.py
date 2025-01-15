from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Product(Base):
    """
    产品模型，用于定义产品表
    """
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(500))
    image: Mapped[str] = mapped_column(String(255), nullable=True)
    category: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"Product(id={self.id!r}, name={self.name!r}, price={self.price!r}, description={self.description!r}, image={self.image!r}, category={self.category!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r}, is_deleted={self.is_deleted!r})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_deleted": self.is_deleted
        }



