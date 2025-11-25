from typing import Optional
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product


def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


def get_products_by_category_ids(db: Session, category_ids: list[int]) -> list[Product]:
    return db.query(Product).filter(Product.category_id.in_(category_ids)).all()

