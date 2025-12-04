from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.crud.crud_user import get_user_by_id
from app.database import get_db
from app.schemas.login import UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("", response_model=TokenResponse, summary="로그인")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user.user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"field": "user_id", "code": "NO_ID"}]
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"field": "password", "code": "INVALID_PASSWORD"}]
        )

    # JWT 발급 (create_access_token 여기서 시간 설정)
    access_token = create_access_token(data={"sub": str(db_user.user_id)})
    refresh_token = create_refresh_token(data={"sub": str(db_user.user_id)})

    return {
        "message": "로그인 성공",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES,
        "user": {
            "name": getattr(db_user, "name", None),
            "user_id": db_user.user_id,
            "role": db_user.role,
        }
    }
