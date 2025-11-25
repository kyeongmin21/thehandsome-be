from sqlalchemy.orm import Session

from app.models.brands import Brands

def get_brands(db: Session):
    return db.query(Brands).order_by(Brands.brand_code).all()