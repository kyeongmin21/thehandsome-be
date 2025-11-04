from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.product import Product  # Product 모델 import
from app.schemas.category import CategoryDetail

router = APIRouter()

# 상위 카테고리 breadcrumb 생성
def build_category_path(category: Category):
    names = []
    while category:
        names.insert(0, category.name)  # 리스트 앞에 추가
        category = category.parent
    return names

# 하위 카테고리까지 모두 ID 가져오기
def get_all_subcategory_ids(category: Category):
    ids = [category.id]
    for child in category.children:
        ids.extend(get_all_subcategory_ids(child))
    return ids

@router.get("/{category_id}", response_model=CategoryDetail)
def get_category_products(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # breadcrumb 생성
    breadcrumb = build_category_path(category)

    # 하위 카테고리까지 포함한 모든 category_id
    subcategory_ids = get_all_subcategory_ids(category)

    # 상품 조회
    products = db.query(Product).filter(Product.category_id.in_(subcategory_ids)).all()

    return {
        "breadcrumb": breadcrumb,
        "products": products
    }
