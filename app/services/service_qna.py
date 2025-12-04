from datetime import datetime
from sqlalchemy.orm import Session
from app.models.qna import Qna, QnaStatus
from app.crud.crud_qna import create_qna, update_qna

def create_qna_service(db: Session, title: str, content: str, author_id: str) -> Qna:
    new_qna = Qna(
        title=title,
        content=content,
        author_id=author_id,
        admin_id=None,
        answer=None,
        status=QnaStatus.pending,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return create_qna(db, new_qna)


def update_qna_service(db: Session, qna: Qna, title: str = None, content: str = None) -> Qna:
    if title is not None:
        qna.title = title
    if content is not None:
        qna.content = content
    qna.updated_at = datetime.utcnow()
    return update_qna(db, qna)


def answer_qna_service(db: Session, qna: Qna, answer: str, admin_id: str) -> Qna:
    qna.answer = answer
    qna.admin_id = admin_id
    qna.status = QnaStatus.answered if answer.strip() else QnaStatus.pending
    qna.updated_at = datetime.utcnow()
    return update_qna(db, qna)
