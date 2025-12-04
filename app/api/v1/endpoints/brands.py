from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.crud.crud_brandlike import get_user_brand_wishes
from app.crud.crud_brands import get_brands
from app.database import get_db
from app.schemas.brands import BrandGroup

router = APIRouter()


# 전체 브랜드 조회
@router.get("/list", response_model=List[BrandGroup], summary="전체 브랜드 조회")
def get_all_brands(request: Request, db: Session = Depends(get_db)):
    brands = get_brands(db)

    # 로그인 되어 있으면 찜 정보 가져오기
    user = getattr(request.state, "user", None)
    wishlist_codes = []
    if user:
        wishlist = get_user_brand_wishes(db, user["id"])
        wishlist_codes = [bl.brand_code for bl in wishlist]

    grouped = {}

    for b in brands:
        grouped.setdefault(b.brand_type, []).append({
            "brand_code": b.brand_code,
            "brand_name": b.brand_name,
            "is_wishlist": b.brand_code in wishlist_codes
        })

    return [
        {"brand_type": k, "brands": v}
        for k, v in grouped.items()
    ]