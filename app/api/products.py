from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from datetime import datetime

router = APIRouter()

summary="[상품] 새로운 상품 등록",
# GET: 전체 상품 조회
@router.get("", response_model=list[ProductOut], summary="[상품] 새로운 상품 등록")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# POST: 상품 추가
@router.post("", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        price=product.price,
        discount_price=product.discount_price,
        discount_rate=product.discount_rate,
        category_id=product.category_id,
        brand=product.brand,
        likes=0,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# PUT: 상품 수정
@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, updated: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="상품 없음")

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(product, key, value)
    product.updated_at = datetime.now()

    db.commit()
    db.refresh(product)
    return product


# DELETE: 상품 삭제
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="상품 없음")
    db.delete(product)
    db.commit()
    return {"message": "상품 삭제 완료"}

