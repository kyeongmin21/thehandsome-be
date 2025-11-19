from fastapi import APIRouter, HTTPException, Depends
from app.database import get_db
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate, ProductItem, ProductCategoryOut
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

router = APIRouter()

# GET: 전체 상품 조회 (그룹핑 포함)
@router.get("", response_model=list[ProductCategoryOut], summary="상품 조회")
def get_products(db: Session = Depends(get_db)):
    # 모든 상품 가져오기
    products = db.query(Product).options(joinedload(Product.category)).all()

    # DB에 존재하는 모든 최상위 카테고리 가져오기
    top_categories = db.query(Category).filter(Category.level == 1).all()

    # 카테고리별 그룹 초기화 (빈 리스트 포함)
    grouped = {c.name: [] for c in top_categories}

    for p in products:
        # 최상위 카테고리 찾기
        top_cat = p.category
        while top_cat.parent:
            top_cat = top_cat.parent
        first_name = top_cat.name

        grouped[first_name].append(ProductItem(
            id=p.id,
            product_code=p.product_code,
            name=p.name,
            price=p.price,
            discount_price=p.discount_price,
            discount_rate=p.discount_rate,
            category_id=p.category_id,
            brand=p.brand,
            likes=p.likes,
            src=p.src
        ))

    # 프론트용 리스트로 변환
    result = [ProductCategoryOut(cate=k, items=v) for k, v in grouped.items()]
    return result

# POST: 상품 추가
@router.post("", response_model=ProductItem, summary="상품 추가")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        product_code=product.product_code,
        name=product.name,
        price=product.price,
        discount_price=product.discount_price,
        discount_rate=product.discount_rate,
        category_id=product.category_id,
        brand=product.brand,
        likes=0,
        src=product.src,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return ProductItem.model_validate(new_product)


# PUT: 상품 수정
@router.put("/{product_id}", response_model=ProductItem, summary="상품 수정")
def update_product(product_id: int, updated: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="상품 없음")

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(product, key, value)
    product.updated_at = datetime.now()

    db.commit()
    db.refresh(product)

    return ProductItem.model_validate(product)


# DELETE: 상품 삭제
@router.delete("/{product_id}", summary="상품 삭제")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="상품 없음")
    db.delete(product)
    db.commit()
    return {"message": "상품 삭제 완료"}

