from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.crud_brands import get_brands
from app.database import get_db
from app.schemas.brands import BrandGroup

router = APIRouter()


# 전체 브랜드 조회
@router.get("/list", response_model=List[BrandGroup], summary="전체 브랜드 조회")
def get_all_brands(db: Session = Depends(get_db)):
    brands = get_brands(db)

    grouped = {}

    for b in brands:
        if b.brand_type not in grouped:
            grouped[b.brand_type] = []

        grouped[b.brand_type].append({
            "brand_code": b.brand_code,
            "brand_name": b.brand_name
        })

    # JSON 형태로 변환
    result = [
        {"brand_type": brand_type, "brands": brand_list}
        for brand_type, brand_list in grouped.items()
    ]

    return result
