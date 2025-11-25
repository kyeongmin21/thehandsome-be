from typing import Optional

from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.wishlist import WishList


def find_user_wishlist(db: Session, user_id: int, product_code: str) -> Optional[WishList]:
    """ 특정 사용자가 특정 상품을 이미 찜했는지 확인할 때 """
    return db.query(WishList).filter(
        WishList.user_id == user_id,
        WishList.product_code == product_code
    ).first()


def get_user_wishlist(db: Session, user_id: int) -> list[tuple[WishList, Product]]:
    """ 사용자의 전체 위시리스트와 상품 정보까지 함께 가져올 때 """
    return (
        db.query(WishList, Product)
        .join(Product, WishList.product_code == Product.product_code)
        .filter(WishList.user_id == user_id)
        .order_by(WishList.created_at.desc())
        .all()
    )


def create_wishlist(db: Session, user_id: int, product_code: str) -> WishList:
    new_wish = WishList(user_id=user_id, product_code=product_code)
    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)
    return new_wish


def delete_wishlist(db: Session, wishlist_item: WishList):
    db.delete(wishlist_item)
    db.commit()
