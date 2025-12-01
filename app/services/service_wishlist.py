from typing import Optional

from sqlalchemy.orm import Session
from app.crud.crud_wishlist import find_user_wishlist, create_wishlist, delete_wishlist, get_user_wishlist
from app.models.user import User
from app.schemas.wishlist import WishListItem

def toggle_wishlist(db: Session, user: User, product_code: str) -> Optional[WishListItem]:
    existing = find_user_wishlist(db, user.id, product_code)

    if existing:
        delete_wishlist(db, existing)
        return None

    new_wish = create_wishlist(db, user.id, product_code)
    product = new_wish.product

    return WishListItem(
        product_code=product.product_code,
        name=product.name,
        price=product.price,
        discount_price=product.discount_price,
        discount_rate=product.discount_rate,
        brand=product.brand,
        src=product.src
    )

def get_my_wishlist(db: Session, user: User) -> list[WishListItem]:
    wishlist_items = get_user_wishlist(db, user.id)

    return [
        WishListItem(
            product_code=product.product_code,
            name=product.name,
            price=product.price,
            discount_price=product.discount_price,
            discount_rate=product.discount_rate,
            brand=product.brand,
            src=product.src
        )
        for wish, product in wishlist_items
    ]