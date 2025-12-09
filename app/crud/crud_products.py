from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional, Dict, Any
from datetime import datetime


def get_products_with_category(db: Session) -> list[type[Product]]:
    """모든 상품을 연결된 카테고리와 함께 조회합니다 (N+1 방지)."""
    return (
        db.query(Product)
        .options(
            joinedload(Product.category)
            .joinedload(Category.parent)  # ← parent 미리 로딩
            .joinedload(Category.parent)  # 부모의 부모까지도 (depth 필요에 따라)
        )
        .order_by(Product.id.asc())
        .all()
    )


def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    """단일 상품을 ID로 조회합니다."""
    return (
        db.query(Product)
        .options(
            joinedload(Product.category)
            .joinedload(Category.parent)
        )
        .filter(Product.id == product_id)
        .first()
    )


def get_top_level_categories(db: Session) -> List[Category]:
    """모든 최상위 레벨 카테고리(level=1)를 조회합니다."""
    return db.query(Category).filter(Category.level == 1).all()


def find_top_category(category: Category) -> Category:
    """주어진 카테고리의 최상위 부모 카테고리를 재귀적으로 찾습니다."""
    if category is None:
        return None
    top_cate = category
    while top_cate.parent:
        top_cate = top_cate.parent
    return top_cate


def create_product_db(db: Session, product_in: ProductCreate) -> Product:
    """새로운 상품 레코드를 데이터베이스에 추가합니다."""
    new_product = Product(
        product_code=product_in.product_code,
        name=product_in.name,
        price=product_in.price,
        discount_price=product_in.discount_price,
        discount_rate=product_in.discount_rate,
        category_id=product_in.category_id,
        brand=product_in.brand,
        likes=0,
        src=product_in.src,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def update_product_db(db: Session, product: Product, product_in: ProductUpdate) -> Product:
    """기존 상품 레코드를 업데이트합니다."""
    update_data: Dict[str, Any] = product_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    product.updated_at = datetime.now()

    db.commit()
    db.refresh(product)
    return product


def delete_product_db(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()
