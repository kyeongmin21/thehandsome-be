from typing import List
from pydantic import BaseModel
from datetime import datetime


# 단일 브랜드 정보를 표현
# 사용되는 곳 : /brands/{id} 단건조회, /brands 전체리스트, 브랜드 생성 & 수정 응답할 때
class BrandItem(BaseModel):
    id: int
    brand_code: str
    brand_name: str
    brand_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# 브랜드 기본 정보 (각 브랜드)
class BrandBasic(BaseModel):
    brand_code: str
    brand_name: str


# 브랜드 타입 기준 그룹
class BrandGroup(BaseModel):
    brand_type: str
    brands: List[BrandBasic]
