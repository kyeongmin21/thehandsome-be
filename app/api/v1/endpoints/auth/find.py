from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.crud.crud_find import get_user_by_email
from app.database import get_db
from app.schemas.find import FindIdResponse, FindIdRequest

router = APIRouter()


@router.post("/id", response_model=FindIdResponse, summary="아이디 찾기")
def find_user_id(req: FindIdRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, req.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="가입된 정보가 없습니다."
        )
    return FindIdResponse(user_id=user.user_id)
