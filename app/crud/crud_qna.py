from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.qna import Qna

def get_qna(db: Session, user_id: Optional[str] = None, is_admin: bool = False) -> List[Qna]:
    if is_admin:
        return db.query(Qna).all()
    return db.query(Qna).filter(Qna.author_id == user_id).all()

def get_qna_by_id(db: Session, qna_id: int) -> Optional[Qna]:
    return db.query(Qna).filter(Qna.id == qna_id).first()

def create_qna(db: Session, qna: Qna) -> Qna:
    db.add(qna)
    db.commit()
    db.refresh(qna)
    return qna

def update_qna(db: Session, qna: Qna) -> Qna:
    db.commit()
    db.refresh(qna)
    return qna

def delete_qna(db: Session, qna: Qna):
    db.delete(qna)
    db.commit()
