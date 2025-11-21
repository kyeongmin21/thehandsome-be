from typing import List, Optional
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status

from app.models.user import User
from app.database import get_db
from app.api.auth.mypage import get_current_user
from app.dependencies.auth_deps import get_optional_user
from app.models.brands import Brands
from app.models.brandlike import BrandLike
from app.schemas.brandlike import BrandCreate, BrandLikeItem

router = APIRouter()


@router.post(
    "/toggle",
    response_model=BrandLikeItem,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_204_NO_CONTENT: {"description": "BrandList item removed"}},
    summary="브랜드 찜 토글: 없으면 추가, 있으면 삭제"
)
def toggle_brand_item(
        data: BrandCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user_id = current_user.id

    # 기존 찜 여부 확인
    existing = db.query(BrandLike).filter(
        BrandLike.user_id == user_id,
        BrandLike.brand_code == data.brand_code
    ).first()

    # 이미 찜되어 있으면 삭제
    if existing:
        db.delete(existing)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # 없으면 새 찜 생성
    new_brand = BrandLike(user_id=user_id, brand_code=data.brand_code)
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)

    # 반환 시 brand_name만 Brands 테이블에서 가져오기
    brand = db.query(Brands).filter(Brands.brand_code == new_brand.brand_code).first()
    return BrandLikeItem(user_id=user_id,
                         brand_code=new_brand.brand_code,
                         brand_name=brand.brand_name if brand else None
                         )


# 내가 찜한 브랜드 리스트 조회
def get_user_brand_wishes(db: Session, user_id: str):
    results = db.query(
        BrandLike.id,
        BrandLike.user_id,
        BrandLike.brand_code,
        Brands.brand_name,
        BrandLike.created_at
    ).join(
        Brands, BrandLike.brand_code == Brands.brand_code
    ).filter(
        BrandLike.user_id == user_id
    ).all()
    return results


@router.get("/my-brands", response_model=List[BrandLikeItem], summary="내가 좋아요한 브랜드 조회")
def get_my_brand_wishes(
        current_user: Optional[User] = Depends(get_optional_user),
        db: Session = Depends(get_db)
):
    if current_user is None:
        return []  # 로그인하지 않았으므로 빈 리스트 반환

    user_pk_id = current_user.id

    # BrandLike와 Brand 조인
    brand_like_items = (
        db.query(BrandLike, Brands)
        .join(Brands, BrandLike.brand_code == Brands.brand_code)
        .filter(BrandLike.user_id == user_pk_id)
        .all()
    )

    return [
        BrandLikeItem(
            user_id=bl.user_id,
            brand_code=bl.brand_code,
            brand_name=b.brand_name
        )
        for bl, b in brand_like_items
    ]
