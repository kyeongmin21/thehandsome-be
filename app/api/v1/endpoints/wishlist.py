from typing import Optional
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.v1.endpoints.auth.mypage import get_current_user
from app.dependencies.auth_deps import get_optional_user
from app.schemas.wishlist import WishListCreate, WishListItem
from app.services import service_wishlist as service_wish

router = APIRouter()


@router.post("/toggle",
             response_model=WishListItem,
             status_code=status.HTTP_201_CREATED,
             responses={status.HTTP_204_NO_CONTENT: {"description": "Wishlist item removed"}},
             summary="상품 위시 토글: 없으면 추가, 있으면 삭제")
def toggle_wishlist_endpoint(data: WishListCreate,
                             current_user=Depends(get_current_user),
                             db: Session = Depends(get_db)):
    result = service_wish.toggle_wishlist(db, current_user, data.product_code)
    if result is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return result


@router.get("/my-wished", response_model=list[WishListItem], summary="내 위시리스트 전체 조회")
def get_my_wishlist_endpoint(current_user: Optional = Depends(get_optional_user),
                             db: Session = Depends(get_db)):
    if current_user is None:
        return []

    return service_wish.get_my_wishlist(db, current_user)
