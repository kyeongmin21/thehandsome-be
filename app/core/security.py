from __future__ import annotations
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
import uuid, os

# ⚠️ 배포 시 반드시 환경 변수로 설정!
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 토큰 유효 시간 (1시간)
REFRESH_TOKEN_EXPIRE_DAYS = 30


# 비밀번호 암호화 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 비밀번호 관련 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """사용자 입력 비밀번호와 해시된 비밀번호 비교"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)


# JWT 토큰 생성 함수
def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """
    JWT 액세스 토큰 생성
    - data: 토큰에 포함할 유저 정보 (예: {"sub": user_id})
    - expires_delta: 만료 시간 (기본 60분)
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    jti = str(uuid.uuid4())  # 토큰 고유 ID (optional)

    to_encode.update({
        "exp": expire,  # 만료 시간
        "iat": datetime.utcnow(),  # 발급 시간
        "jti": jti,  # JWT ID (고유 식별자)
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# refresh 토큰 생성 함수
def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    jti = str(uuid.uuid4())
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": jti,
        "typ": "refresh"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 토큰 디코딩 함수
def decode_jwt_token(token: str) -> dict:
    """
    JWT 토큰 디코딩
    - 유효하지 않거나 만료되면 예외 발생
    - 정상일 경우 payload(dict) 반환
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e