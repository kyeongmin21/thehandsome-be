import secrets
from typing import Optional
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import decode_jwt_token
from app.models.user import User


def generate_ci(length: int = 10) -> str:
    """
    안전한 랜덤 10자리 문자열 생성
    - 16진수 기반 (0-9, a-f)
    - ex: '03ceccb055'
    """
    return secrets.token_hex(length // 2)


def get_optional_token(request: Request):
    auth = request.headers.get("Authorization")
    if auth and auth.startswith("Bearer "):
        return auth.split(" ")[1]
    return None


def get_optional_user(
    token: Optional[str] = Depends(get_optional_token),
    db: Session = Depends(get_db)
):
    if token is None:
        return None  # 로그인 안 한 사용자

    try:
        payload = decode_jwt_token(token)
        user = db.query(User).filter(User.user_id == payload.get("sub")).first()

        if not user:
            return None
        if not user.is_active:
            return None

        return user
    except:
        return None  # 토큰 이상 → 그냥 None