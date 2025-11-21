from typing import Optional

from pydantic import BaseModel


# 좋아요 브랜드 “추가 or 토글” 할 때 사용
# 프론트 -> 백엔드
class BrandCreate(BaseModel):
    brand_code: str


# 백엔드 -> 프론트
class BrandLikeItem(BaseModel):
    user_id: int
    brand_code: str
    brand_name: Optional[str] = None

    class Config:
        from_attributes = True
