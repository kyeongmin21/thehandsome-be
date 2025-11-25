from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import service_category
from app.schemas.category import CategoryDetail

router = APIRouter()

@router.get("/{category_id}", response_model=CategoryDetail)
def get_category_products(category_id: int, db: Session = Depends(get_db)):
    result = service_category.get_category_with_products(db, category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return result
