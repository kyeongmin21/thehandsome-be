from pydantic import BaseModel
from typing import List, Optional

# 상품 생성용 데이터 (프론트에서 보내는 입력)
class ProductCreate(BaseModel):
    product_code: str
    name: str
    price: int
    discount_price: Optional[int] = None
    discount_rate: Optional[float] = None
    category_id: int
    brand: Optional[str] = None
    src: Optional[str] = None

# 상품 수정용 데이터
class ProductUpdate(BaseModel):
    product_code: Optional[str] = None
    name: Optional[str] = None
    price: Optional[int] = None
    discount_price: Optional[int] = None
    discount_rate: Optional[float] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    likes: Optional[int] = None
    src: Optional[str] = None


# 단일 상품 반환용
class ProductItem(BaseModel):
    product_code: str
    id: int
    name: str
    price: int
    discount_price: Optional[int] = None
    discount_rate: Optional[float] = None
    category_id: int
    brand: Optional[str] = None
    likes: int
    src: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


# 카테고리별 상품 묶음 반환용
class ProductCategoryOut(BaseModel):
    cate: str
    items: List[ProductItem] = []

    model_config = {
        "from_attributes": True
    }