from sqlalchemy import Column, Integer, Enum, String, Boolean, DateTime, func
from app.database import Base
from sqlalchemy.orm import relationship
import enum, string, secrets
from app.models.qna import Qna

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

def generate_client_id(length: int = 10) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# --- User 모델 정의 ---
class User(Base):
    __tablename__ = "users"

    # 필수 필드
    ci = Column(String, unique=True, default=generate_client_id, nullable=False)
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
    deleted_at = Column(DateTime, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.client, nullable=False)
    login_type = Column(Enum(LoginType), default=LoginType.general, nullable=False)
    membership_grade = Column(Enum(MembershipGrade), default=MembershipGrade.family, nullable=False)

    qna = relationship(
        "Qna",
        back_populates="author",      # Qna.author와 연결
        foreign_keys=[Qna.author_id]  # 어떤 FK를 기준으로 매핑할지 명시
    )