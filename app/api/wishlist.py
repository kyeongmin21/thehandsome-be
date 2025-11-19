from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status

from app.api.auth.mypage import get_current_user
from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.models.wishlist import WishList
from app.schemas.wishlist import WishListCreate, WishListItem

router = APIRouter()


@router.post("/toggle",
             response_model=WishListItem,
             status_code=status.HTTP_201_CREATED,  # 생성(추가) 시 201을 명시
             responses={
                 status.HTTP_204_NO_CONTENT: {"description": "Wishlist item removed"}  # 삭제 시 204 명시
             },
             summary="상품 위시 토글: 없으면 추가, 있으면 삭제")
def toggle_wishlist(data: WishListCreate,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):

    user_id = current_user.id

    # 기존 위시가 있는지 확인
    existing = db.query(WishList).filter(
        WishList.user_id == user_id,
        WishList.product_code == data.product_code
    ).first()

    # 삭제 로직
    if existing:
        db.delete(existing)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)  # 삭제되었더라도 기존 데이터 응답

    # 생성 로직
    new_wish = WishList(user_id=user_id, product_code=data.product_code)
    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)

    # 상품 정보 함께 반환
    product = db.query(Product).filter(Product.product_code == data.product_code).first()

    return WishListItem(
        product_code=product.product_code,
        name=product.name,
        price=product.price,
        discount_price=product.discount_price,
        discount_rate=product.discount_rate,
        brand=product.brand,
        src=product.src
    )

@router.get("/my", response_model=list[WishListItem], summary="내 위시리스트 전체 조회")
def get_my_wishlist(current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    user_pk_id = current_user.id

    # WishList와 Product 조인
    wishlist_items = (
        db.query(WishList, Product)
        .join(Product, WishList.product_code == Product.product_code)
        .filter(WishList.user_id == user_pk_id)  # 내 위시만
        .order_by(WishList.created_at.desc())  # 최근 찜 순
        .all()
    )

    result = [
        WishListItem(
            product_code=item.Product.product_code,
            name=item.Product.name,
            price=item.Product.price,
            discount_price=item.Product.discount_price,
            discount_rate=item.Product.discount_rate,
            brand=item.Product.brand,
            src=item.Product.src
        )
        for item in wishlist_items
    ]

    return result