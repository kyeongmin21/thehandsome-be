from pydantic import BaseModel
from typing import Optional, List

class CategoryRead(BaseModel):
    id: int
    name: str
    price: Optional[int] = None
    discount_price: Optional[int] = None
    discount_rate: Optional[float] = None
    brand: Optional[str] = None
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True

class CategoryDetail(BaseModel):
    breadcrumb: List[str]
    products: List[CategoryRead]