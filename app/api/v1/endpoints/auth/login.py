from __future__ import annotations
from fastapi import APIRouter, Depends, Response, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.crud.crud_user import get_user_by_id
from app.database import get_db
from app.schemas.login import UserLogin, TokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("", response_model=TokenResponse, summary="로그인")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
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


    # 리프레시 토큰은 HttpOnly, Secure 쿠키로 클라이언트에 설정 (JS에서 접근 불가): 장기 인증/재발급용
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # JS에서 접근 불가 → 보안 강화
        secure=False,   # HTTPS 환경에서만 전송: secure=True일 경우 로컬 http에서 안 내려올 수 있음 → secure=False로 테스트
        path="/",       # 모든 경로에서 쿠키 사용 가능하도록 설정
        max_age=7 * 24 * 3600,
        samesite="Lax"
    )

    return {
        "message": "로그인 성공",
        "access_token": access_token,
        "expires_in": 30 * 60,  # 30분
        "user": {
            "name": getattr(db_user, "name", None),
            "user_id": db_user.user_id,
            "role": db_user.role,
        }
    }
