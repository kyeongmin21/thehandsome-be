from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum as PyEnum

class UserLoginType(PyEnum):
    GENERAL = "general"
    KAKAO = "kakao"

# 1. 회원가입 요청 데이터 (클라이언트 -> 서버)
class UserCreate(BaseModel):
    name: str = Field(..., description="사용자 이름")
    email: EmailStr = Field(..., description="사용자 이메일")
    id: str = Field(..., description="사용자 아이디")
    password: str = Field(..., description="사용자 비밀번호")
    phone: str = Field(..., description="사용자 휴대폰 번호")

    login_type: UserLoginType = Field(..., description="로그인 타입 (general 또는 kakao)")

# 2. 회원정보 수정 데이터 (클라이언트 -> 서버)
# 수정은 선택적이므로 모든 필드를 Optional로 설정합니다.
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[EmailStr] = None
    phone: Optional[str] = None


# 3. 응답 데이터 (서버 -> 클라이언트)
class UserOut(BaseModel):
    # 비밀번호를 제외한 정보만 클라이언트에게 보냅니다.
    name: str
    email: EmailStr
    id: str
    phone: str

    login_type: UserLoginType

    class Config:
        # SQLAlchemy 모델을 Pydantic으로 변환할 때 필요합니다.
        from_attributes = True