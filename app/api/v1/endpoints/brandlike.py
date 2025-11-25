from typing import List, Optional
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status

from app.models.user import User
from app.database import get_db
from app.api.v1.endpoints.auth.mypage import get_current_user
from app.dependencies.auth_deps import get_optional_user
from app.schemas.brandlike import BrandCreate, BrandLikeItem
from app.crud.crud_brandlike import (
    get_brand_like, delete_brand_like, create_brand_like,
    get_user_brand_wishes, get_brand_info
)

router = APIRouter()


@router.post("/toggle", response_model=BrandLikeItem)
def toggle_brand_item(
    data: BrandCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id

    # 기존 여부 확인
    existing = get_brand_like(db, user_id, data.brand_code)

    if existing:
        delete_brand_like(db, existing)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # 생성
    new_item = create_brand_like(db, user_id, data.brand_code)

    # brand_name 조회
    brand_info = get_brand_info(db, new_item.brand_code)

    return BrandLikeItem(
        user_id=user_id,
        brand_code=new_item.brand_code,
        brand_name=brand_info.brand_name if brand_info else None
    )


@router.get("/my-brands", response_model=List[BrandLikeItem])
def get_my_brand_wishes_route(
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    if current_user is None:
        return []

    items = get_user_brand_wishes(db, current_user.id)

    return [
        BrandLikeItem(
            user_id=bl.user_id,
            brand_code=bl.brand_code,
            brand_name=b.brand_name
        )
        for bl, b in items
    ]
