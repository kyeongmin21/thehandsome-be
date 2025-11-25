from sqlalchemy.orm import Session
from app.crud import crud_products as crud_product
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductItem, ProductCategoryOut
from typing import List


def get_grouped_products(db: Session) -> List[ProductCategoryOut]:
    """
    모든 상품을 조회하고 최상위 카테고리 기준으로 그룹핑하여 반환하는 비즈니스 로직.
    """
    # 1. CRUD를 통해 데이터 조회
    products: List[Product] = crud_product.get_products_with_category(db)
    top_categories = crud_product.get_top_level_categories(db)

    # 2. 카테고리별 그룹 초기화
    grouped = {c.name: [] for c in top_categories}

    # 3. 그룹핑 로직 실행
    for p in products:
        if p.category:
            # CRUD에 정의된 헬퍼 함수를 사용하여 최상위 카테고리 이름 가져오기
            top_cat = crud_product.find_top_category(p.category)
            first_name = top_cat.name

            # Pydantic 스키마로 변환
            product_item = ProductItem.model_validate(p)

            # 그룹에 추가
            if first_name in grouped:
                grouped[first_name].append(product_item)

    # 4. 최종 응답 형식으로 변환
    return [ProductCategoryOut(cate=k, items=v) for k, v in grouped.items()]


def create_new_product(db: Session, product_in: ProductCreate) -> Product:
    return crud_product.create_product_db(db, product_in)


def update_existing_product(db: Session, product_id: int, product_in: ProductUpdate) -> Product:
    product = crud_product.get_product_by_id(db, product_id)
    if not product:
        # Service Layer는 DB 관련 예외만 발생시키고, HTTP 예외는 Endpoint에서 처리합니다.
        # 여기서는 None을 반환하여 Endpoint가 404를 발생시키도록 합니다.
        return None

    return crud_product.update_product_db(db, product, product_in)


def delete_existing_product(db: Session, product_id: int) -> bool:
    product = crud_product.get_product_by_id(db, product_id)
    if not product:
        return False  # 삭제할 상품 없음

    crud_product.delete_product_db(db, product)
    return True
