from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.crud_qna import get_qna_by_id, delete_qna
from app.services.service_qna import create_qna_service, update_qna_service, answer_qna_service
from app.database import get_db
from app.models.qna import Qna
from app.models.user import User, UserRole
from app.api.v1.endpoints.auth.mypage import get_current_user
from app.schemas.qna import QnaCreate, QnaAnswerRequest, QnaResponse, QnaUpdate

router = APIRouter()


@router.get('/qna', response_model=List[QnaResponse], summary='1:1 문의 리스트')
def get_qna(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # 로그인한 유저 정보
):
    if current_user.role == UserRole.admin:
        qnas = db.query(Qna).all()
    else:
        qnas = db.query(Qna).filter(Qna.author_id == current_user.user_id).all()

    # ORM -> Pydantic 변환
    return [QnaResponse.from_orm_with_label(qna) for qna in qnas]


@router.get("/qna/{qna_id}", response_model=QnaResponse, summary="내가 쓴 1:1 문의 단일 조회")
def get_my_qna(
        qna_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    qna = get_qna_by_id(db, qna_id)
    if not qna:
        raise HTTPException(status_code=404, detail="QnA를 찾을 수 없습니다.")

    if current_user.role == UserRole.admin:
        pass
    elif current_user.role == UserRole.client:
        if qna.author_id != current_user.user_id:
            raise HTTPException(status_code=403, detail="본인 글만 조회할 수 있습니다.")
    else:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    return QnaResponse.from_orm_with_label(qna)


@router.post("/qna/create", response_model=QnaResponse, summary='client 1:1 문의 등록')
def create_qna(
        qna_request: QnaCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # 클라이언트만 등록 가능
    if current_user.role != UserRole.client:
        raise HTTPException(status_code=403, detail="일반 회원만 문의를 등록할 수 있습니다.")

    new_qna = create_qna_service(db, qna_request.title, qna_request.content, current_user.user_id)
    return QnaResponse.from_orm_with_label(new_qna)


# admin - 기존 문의글에 “답변”을 등록
@router.post("/qna/{qna_id}/answer", response_model=QnaAnswerRequest, summary='admin 1:1 문의 답글')
def create_qna_answer(
        qna_id: int,
        answer_request: QnaAnswerRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # ← 로그인된 관리자
):
    #  관리자 권한 확인
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="관리자만 답변할 수 있습니다.")

    # 해당 QnA 찾기
    qna = get_qna_by_id(db, qna_id)
    if not qna:
        raise HTTPException(status_code=404, detail="QnA를 찾을 수 없습니다.")

    # 답변 등록
    answered_qna = answer_qna_service(db, qna, answer_request.answer, current_user.user_id)
    return QnaResponse.from_orm_with_label(answered_qna)


@router.put("/qna/{qna_id}", response_model=QnaResponse, summary="client 1:1 문의 수정")
def update_qna(qna_id: int, qna_request: QnaUpdate, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    qna = get_qna_by_id(db, qna_id)
    if not qna:
        raise HTTPException(status_code=404, detail="QnA를 찾을 수 없습니다.")
    if qna.author_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="본인 글만 수정할 수 있습니다.")

    updated_qna = update_qna_service(db, qna, qna_request.title, qna_request.content)
    return QnaResponse.from_orm_with_label(updated_qna)


@router.delete("/qna/{qna_id}", summary="내가 쓴 1:1 문의 삭제")
def delete_qna(
        qna_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    qna = get_qna_by_id(db, qna_id)
    if not qna:
        raise HTTPException(status_code=404, detail="QnA를 찾을 수 없습니다.")

    # 작성자 본인만 삭제 가능
    if qna.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="본인 글만 삭제할 수 있습니다.")

    delete_qna(db, qna)
    return {"detail": "삭제되었습니다."}
