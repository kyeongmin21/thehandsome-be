from sqlalchemy.orm import Session

from app.models.brandlike import BrandLike
from app.models.brands import Brands


def get_brand_like(db: Session, user_id: int, brand_code: str):
    return (
        db.query(BrandLike)
        .filter(BrandLike.user_id == user_id,
                BrandLike.brand_code == brand_code)
        .first()
    )


def get_brand_info(db: Session, brand_code: str):
    return (
        db.query(Brands)
        .filter(Brands.brand_code == brand_code)
        .first()
    )


def get_user_brand_wishes(db: Session, user_id: int):
    return (
        db.query(BrandLike, Brands)
        .join(Brands, BrandLike.brand_code == Brands.brand_code)
        .filter(BrandLike.user_id == user_id)
        .all()
    )


def create_brand_like(db: Session, user_id: int, brand_code: str):
    new_brand = BrandLike(user_id=user_id, brand_code=brand_code)
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand


def delete_brand_like(db: Session, brand_like: BrandLike):
    db.delete(brand_like)
    db.commit()
