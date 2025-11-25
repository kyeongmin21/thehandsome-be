
from app.models.category import Category
from app.crud import crud_category as crud_cate

def build_category_path(category: Category) -> list[str]:
    """상위 카테고리까지 경로 생성"""
    path = []
    current = category
    while current:
        path.insert(0, current.name)
        current = current.parent
    return path

def get_all_subcategory_ids(category: Category) -> list[int]:
    """하위 카테고리까지 포함한 모든 카테고리 ID 조회"""
    ids = [category.id]
    for child in category.children:
        ids.extend(get_all_subcategory_ids(child))
    return ids

def get_category_with_products(db, category_id: int) -> dict:
    """카테고리와 해당 카테고리 + 하위 카테고리 상품 조회"""
    category = crud_cate.get_category(db, category_id)
    if not category:
        return None

    breadcrumb = build_category_path(category)
    category_ids = get_all_subcategory_ids(category)
    products = crud_cate.get_products_by_category_ids(db, category_ids)

    return {"breadcrumb": breadcrumb, "products": products}
