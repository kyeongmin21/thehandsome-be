from typing import Optional
from pydantic import BaseModel

class UserLogin(BaseModel):
    user_id: str
    password: str


# 토큰 응답에 포함되는 사용자 정보 스키마
class UserInfo(BaseModel):
    user_id: str
    name: Optional[str] = None
    role: Optional[str] = None


# 로그인 및 토큰 재발급 응답 스키마
class TokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
    user: UserInfo