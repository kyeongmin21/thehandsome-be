from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.qna import QnaStatus, QNA_STATUS_LABELS


# 1. 생성 (프론트 → 서버)
class QnaCreate(BaseModel):
    title: str
    content: str


# 2. 수정
class QnaUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# 3. 관리자 답변
class QnaAnswerRequest(BaseModel):
    answer: str


# 4. 응답 (서버 → 프론트)
class QnaResponse(BaseModel):
    id: int
    title: str
    content: str
    answer: Optional[str]
    admin_id: Optional[str] = None
    author_id: str
    status: QnaStatus
    status_label: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    # 👇️ 이 부분이 CRITICAL FIX 입니다!
    model_config = ConfigDict(
        from_attributes=True  # ORM 객체에서 속성(Attribute)을 읽어오도록 허용
    )

    # 자동으로 status_label 설정
    @classmethod
    def from_orm_with_label(cls, qna):
        """ORM 객체에서 자동 변환 + 한글 상태 추가"""
        response = cls.model_validate(qna)
        response.status_label = QNA_STATUS_LABELS.get(qna.status, "")
        return response