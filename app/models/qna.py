from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# 상태 Enum
class QnaStatus(str, enum.Enum):
    pending = "pending"
    reviewing = "reviewing"
    answered = "answered"

# 딕셔너리 매핑 : 한글로 보여줄 때 쓰는 매핑
QNA_STATUS_LABELS = {
    QnaStatus.pending: "답변전",
    QnaStatus.reviewing: "확인중",
    QnaStatus.answered: "답변완료",
}

class Qna(Base):
    __tablename__ = "qna"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    # 관리자 답변 관련
    answer = Column(Text, nullable=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    admin = relationship("User", foreign_keys=[admin_id])  # 답변한 관리자

    # 작성자
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship(
        "User",
        foreign_keys=[author_id],
        back_populates="qna"  # User 모델에서 qna와 매칭
    )

    status = Column(Enum(QnaStatus), default=QnaStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

