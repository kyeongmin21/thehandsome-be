from sqlalchemy import Column, Integer, Enum, String, Boolean, DateTime
from app.database import Base
from datetime import datetime
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    CLIENT = "client"
    GUEST = "guest"

class UserLoginType(enum.Enum):
    GENERAL = "general" # 일반 회원가입
    KAKAO = "kakao"

class MembershipGrade(enum.Enum):
    FAMILY = "family"
    SILVER = "silver"
    GOLD = "gold"
    VIP = "vip"

class User(Base):
    __tablename__ = "users"

    # 필수 필드
    id = Column(Integer, primary_key=True, index=True)  # DB 내부용 Primary Key
    user_id = Column(String, unique=True, index=True, nullable=False)  # 프론트에서 넘어온 ID
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # 비밀번호는 해시되어 저장
    phone = Column(String, nullable=False)

    # 추가 필드 (고려해볼 만한 필드)
    address = Column(String, nullable=True)
    marketing_agree = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)  # 계정 활성화 여부 (탈퇴 시 유용)
    birth_date = Column(DateTime, nullable=True)
    login_type = Column(Enum(UserLoginType), default=UserLoginType.GENERAL, nullable=False)  # 일반회원가입 / 카카오
    membership_grade = Column(Enum(MembershipGrade), default=MembershipGrade.FAMILY, nullable=False  )
    point = Column(Integer, default=0, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False) # 권한 admin / client / guest

