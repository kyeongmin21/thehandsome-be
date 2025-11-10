from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from pydantic import BaseModel, EmailStr

router = APIRouter()

# 요청 DTO
class FindIdRequest(BaseModel):
    email: EmailStr  # 이메일로 아이디 찾기

# 응답 DTO
class FindIdResponse(BaseModel):
    user_id: str

@router.post("/id", response_model=FindIdResponse, summary="아이디 찾기")
def find_user_id(req: FindIdRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.email == req.email, User.is_active == True)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="가입된 정보가 없습니다."
        )
    return FindIdResponse(user_id=user.user_id)
