from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.services import service_products as service_product
from app.schemas.product import ProductCreate, ProductUpdate, ProductItem, ProductCategoryOut, ProductListResponse, \
    ProductSort
from typing import List
import math

router = APIRouter()


### GET: 전체 상품 조회 (메인페이지) ###
@router.get("/grouped", response_model=List[ProductCategoryOut], summary="메인페이지 상품 조회")
def get_products_grouped_api(db: Session = Depends(get_db)):
    """Service 계층에 그룹핑 로직을 위임합니다."""
    return service_product.get_grouped_products(db)


# 상품리스트 페이지 조회
@router.get("", response_model=ProductListResponse, summary="리스트페이지 상품 조회 (페이지네이션)")
def get_products_list_api(
        main: str = None,
        sub: str = None,
        page: int = Query(1, ge=1),
        size: int = Query(8, ge=1, le=50),
        sort: ProductSort = Query(ProductSort.latest),
        db: Session = Depends(get_db)
):
    query = db.query(Product)

    if main:
        # 메인 카테고리 찾기
        main_category = db.query(Category).filter(
            Category.name == main,
            Category.level == 1
        ).first()

        if main_category:
            if sub:
                # 서브 카테고리로 필터링
                sub_category = db.query(Category).filter(
                    Category.name == sub,
                    Category.parent_id == main_category.id
                ).first()

                if sub_category:
                    query = query.filter(Product.category_id == sub_category.id)
            else:
                # sub가 없으면: 서브 카테고리가 있는지 확인
                sub_ids = db.query(Category.id).filter(
                    Category.parent_id == main_category.id
                ).all()
                sub_ids = [sid[0] for sid in sub_ids]

                if sub_ids:
                    # 서브 카테고리가 있으면 그것들로 필터링
                    query = query.filter(Product.category_id.in_(sub_ids))
                else:
                    # 서브 카테고리가 없으면 메인 카테고리 ID로 필터링
                    query = query.filter(Product.category_id == main_category.id)


    # 1. 정렬
    if sort == ProductSort.price_asc:
        query = query.order_by(asc(Product.price))
    elif sort == ProductSort.price_desc:
        query = query.order_by(desc(Product.price))
    elif sort == ProductSort.latest:
        query = query.order_by(desc(Product.created_at))

    # 2. count
    total_count = query.count()
    total_pages = math.ceil(total_count / size)

    # 3. pagination
    products = (
        query
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return {
        "items": products,
        "page": page,
        "size": size,
        "sort": sort,
        "totalCount": total_count,
        "totalPages": total_pages
    }


### POST: 상품 추가 ###
@router.post("", response_model=ProductItem, summary="상품 추가", status_code=status.HTTP_201_CREATED)
def create_product_api(product: ProductCreate, db: Session = Depends(get_db)):
    """Service 계층을 통해 상품을 생성합니다."""
    new_product = service_product.create_new_product(db, product)
    return new_product


### PUT: 상품 수정 ###
@router.put("/{product_id}", response_model=ProductItem, summary="상품 수정")
def update_product_api(product_id: int, updated: ProductUpdate, db: Session = Depends(get_db)):
    """Service 계층을 통해 상품을 수정하고, 상품이 없을 경우 404를 반환합니다."""
    updated_product = service_product.update_existing_product(db, product_id, updated)

    if not updated_product:
        raise HTTPException(status_code=404, detail="상품 없음")

    return updated_product


### DELETE: 상품 삭제 ###
@router.delete("/{product_id}", summary="상품 삭제", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_api(product_id: int, db: Session = Depends(get_db)):
    """Service 계층을 통해 상품을 삭제하고, 상품이 없을 경우 404를 반환합니다."""
    success = service_product.delete_existing_product(db, product_id)

    if not success:
        raise HTTPException(status_code=404, detail="상품 없음")

    return
