from pydantic import BaseModel
from typing import Optional

# 상품 생성용 데이터 (프론트에서 보내는 입력)
class ProductCreate(BaseModel):
    name: str
    price: int
    discount_price: Optional[int] = None
    discount_rate: Optional[float] = None
    category_id: int
    brand: Optional[str] = None

# 상품 수정용 데이터
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    discount_price: Optional[int] = None
    discount_rate: Optional[float] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    likes: Optional[int] = None

# DB에서 가져와서 프론트로 내려줄 때
class ProductOut(BaseModel):
    id: int
    name: str
    price: int
    discount_price: Optional[int]
    discount_rate: Optional[float]
    category_id: int
    brand: Optional[str]
    likes: int

    class Config:
        orm_mode = True
