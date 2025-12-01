from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class BrandLike(Base):
    __tablename__ = "brand_like"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    brand_code = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
