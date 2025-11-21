from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from app.database import Base


class Brands(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand_code = Column(String(100), ForeignKey("brands.brand_code"), nullable=False)
    brand_name = Column(String(100), nullable=False)
    brand_type = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
