from sqlalchemy import Column, Integer, Enum, String, Boolean, DateTime, func
from app.database import Base
import enum

class UserRole(enum.Enum):
    admin = "admin"
    client = "client"
    guest = "guest"

class LoginType(enum.Enum):
    general = "general"  # 일반 회원가입
    kakao = "kakao"

class MembershipGrade(enum.Enum):
    family = "family"
    silver = "silver"
    gold = "gold"
    vip = "vip"


# --- User 모델 정의 ---
class User(Base):
    __tablename__ = "users"

    # 필수 필드
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String, nullable=False)

    # 추가 필드
    address = Column(String, nullable=True)
    marketing_agree = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    birth_date = Column(DateTime, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.client, nullable=False)
    login_type = Column(Enum(LoginType), default=LoginType.general, nullable=False)
    membership_grade = Column(Enum(MembershipGrade), default=MembershipGrade.family, nullable=False)

