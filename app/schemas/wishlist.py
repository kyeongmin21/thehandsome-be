from typing import Optional
from pydantic import BaseModel

# 위시 “추가 or 토글” 할 때 사용
class WishListCreate(BaseModel):
    product_code: str

# 상품 위시리스트 데이터
class WishListItem(BaseModel):
    product_code: str
    name: str
    price: int
    discount_price: Optional[int] = None
    discount_rate: Optional[float] = None
    brand: Optional[str] = None
    src: Optional[str] = None

    class Config:
        from_attributes = True