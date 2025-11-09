from __future__ import annotations
from fastapi import APIRouter, Depends, Response, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from app.database import get_db
from app.models.user import User
from app.schemas.login import UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("", response_model=TokenResponse)
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = (
        db.query(User)
        .filter(User.user_id == user.user_id)
        .first()
    )

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

    # JWT 발급
    access_token = create_access_token(data={"sub": db_user.user_id})
    refresh_token = create_refresh_token(data={"sub": str(db_user.user_id)})

    # 리프레시 토큰은 HttpOnly, Secure 쿠키로 클라이언트에 설정 (JS에서 접근 불가)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,    # HTTPS 환경에서만 전송: secure=True일 경우 로컬 http에서 안 내려올 수 있음 → secure=False로 테스트
        samesite="lax",  # 또는 "strict" / "none" (도메인/요구에 따라) CSRF 방어에 도움
        max_age=30 * 24 * 3600
    )

    return {
        "message": "로그인 성공",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "name": getattr(db_user, "name", None),
            "user_id": db_user.user_id,
        }
    }
