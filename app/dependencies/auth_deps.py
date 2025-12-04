import secrets, os
from jose import JWTError, jwt
from typing import Optional
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import decode_jwt_token
from app.models.user import User
from app.crud.crud_user import get_user_by_id

def generate_ci(length: int = 10) -> str:
    """
    안전한 랜덤 10자리 문자열 생성
    - 16진수 기반 (0-9, a-f)
    - ex: '03ceccb055'
    """
    return secrets.token_hex(length // 2)


# /token 경로에서 로그인 시 토큰 발급
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # <-- 이 부분이 헤더 사용을 기본으로 함
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_me")
ALGORITHM = "HS256"
# 현재 로그인 사용자 가져오기
# oauth2_scheme (즉, Authorization: Bearer <token>) 방식으로 가져옴
def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    """
    액세스 토큰을 검증하고 유효하며 활성 상태인 사용자 객체를 반환합니다.
    유효하지 않거나 비활성 상태이면 401 Unauthorized를 발생시킵니다.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = get_user_by_id(db, payload.get("sub"))

        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        if not user.is_active:
            raise HTTPException(status_code=401, detail="Inactive user")
        return user

    except jwt.ExpiredSignatureError:
        # 토큰 만료 시, 401 Unauthorized를 명시적으로 반환
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired. Please refresh.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        # 위변조(JWTError): 토큰이 무효함 > 갱신 불가능 > 곧바로 로그아웃 유도
        raise credentials_exception



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