from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut

router = APIRouter()

# 비밀번호 해싱 함수 정의
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# POST: 사용자 생성
@router.post("/", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    new_user = User(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        hashed_password=hashed_pw,
        phone=user.phone,
    )

    db.add(new_user)
    db.commit() # DB에 변경사항 반영 (저장)
    db.refresh(new_user)

    return new_user
