from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)  # 상품명
    price = Column(Integer, nullable=False)     # 원가/정가
    discount_price = Column(Integer)            # 할인 가격
    discount_rate = Column(Float)               # 할인율 (%)
    category_id = Column(Integer, ForeignKey("categories.id"))  # 카테고리 연결
    brand = Column(String(100))                 # 브랜드
    likes = Column(Integer, default=0)          # 좋아요 수
