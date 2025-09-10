from fastapi import APIRouter, HTTPException
router = APIRouter()

# 샘플 상품 데이터
products = [
    {"id": 1, "name": "화이트 셔츠", "price": 30000},
    {"id": 2, "name": "블루 데님 팬츠", "price": 45000},
    {"id": 3, "name": "블랙 자켓", "price": 75000},
    {"id": 4, "name": "블랙 자켓", "price": 75000},
]

# GET: 전체 상품 조회
@router.get("")
def get_products():
    return products


# POST: 상품 추가
@router.post("/products")
def create_product(product: dict):
    products.append(product) # append(x) 는 리스트 맨 뒤에 x 를 추가
    return {"message": "상품 추가 완료"}

#PUT: 상품 수정
@router.put("/products/{product_id}")
def update_product(product_id: int, updated: dict):
    for product in products:
        if product["id"] == product_id:
            product.update(updated)
            return {"message": "상품 수정 완료"}
    return HTTPException(status_code=404, detail="상품 없음")

#DELETE: 상품 삭제
@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    for i, p in enumerate(products):
        if p["id"] == product_id:
            products.pop(i)
            return {"message": "상품 삭제 완료"}
    raise HTTPException(status_code=404, detail="상품 없음")