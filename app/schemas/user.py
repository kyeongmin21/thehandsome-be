from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from app.models.user import UserRole, LoginType, MembershipGrade


# 1. 회원가입 요청 데이터 (클라이언트 -> 서버)
class UserCreate(BaseModel):
    name: str = Field(..., description="사용자 이름")
    email: EmailStr = Field(..., description="사용자 이메일")
    user_id: str = Field(..., description="사용자 아이디")
    password: str = Field(..., description="사용자 비밀번호")
    phone: str = Field(..., description="사용자 휴대폰 번호")
    role: Optional[UserRole] = Field(default=UserRole.client, description="사용자 권한 (기본 CLIENT)")
    login_type: Optional[LoginType] = Field(default=LoginType.general, description="로그인 타입 (general 또는 kakao)")
    membership_grade: Optional[MembershipGrade] = Field(default=MembershipGrade.family, description="기본 회원 등급")


# 2. 회원정보 수정 데이터 (클라이언트 -> 서버)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    login_type: Optional[LoginType] = None
    membership_grade: Optional[MembershipGrade] = None


# 3. 응답 데이터 (서버 -> 클라이언트)
class UserOut(BaseModel):
    name: str
    email: EmailStr # 이메일 형식 자동 검증
    user_id: str
    phone: str
    role: UserRole
    login_type: LoginType
    membership_grade: MembershipGrade

    class Config:
        # SQLAlchemy 모델을 Pydantic으로 변환할 때 필요합니다.
        from_attributes = True