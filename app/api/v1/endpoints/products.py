from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import service_products as service_product
from app.schemas.product import ProductCreate, ProductUpdate, ProductItem, ProductCategoryOut
from typing import List

router = APIRouter()


### GET: 전체 상품 조회 ###
@router.get("", response_model=List[ProductCategoryOut], summary="상품 조회")
def get_products_api(db: Session = Depends(get_db)):
    """Service 계층에 그룹핑 로직을 위임합니다."""
    return service_product.get_grouped_products(db)


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
