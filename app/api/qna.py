from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth.mypage import get_current_user
from app.database import get_db
from app.models.qna import Qna, QnaStatus
from app.models.user import User,UserRole
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
        qnas = db.query(Qna).filter(Qna.author_id == current_user.id).all()

        # ORM -> Pydantic 변환
    return [QnaResponse.from_orm_with_label(qna) for qna in qnas]


@router.get("/qna/{qna_id}", response_model=QnaResponse, summary="내가 쓴 1:1 문의 단일 조회")
def get_my_qna(
    qna_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # QnA 조회
    qna = db.query(Qna).filter(Qna.id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA를 찾을 수 없습니다.")

    # 작성자 본인 확인
    if qna.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="본인 글만 조회할 수 있습니다.")

    return QnaResponse.from_orm_with_label(qna)


@router.post("/qna/create", response_model=QnaResponse, summary='client 1:1 문의 등록')
def create_qna(
    qna_request: QnaCreate,  # ← 여긴 질문용 새 스키마 만들어줄 거야!
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 클라이언트만 등록 가능
    if current_user.role != UserRole.client:
        raise HTTPException(status_code=403, detail="일반 회원만 문의를 등록할 수 있습니다.")

    new_qna = Qna(
        title=qna_request.title,
        content=qna_request.content,
        author_id=current_user.id,
        status=QnaStatus.pending,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_qna)
    db.commit()
    db.refresh(new_qna)

    return QnaResponse.from_orm_with_label(new_qna)



@router.put("/qna/{qna_id}", response_model=QnaResponse, summary="client 1:1 문의 수정")
def update_qna(
    qna_id: int,
    qna_request: QnaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 기존 QnA 조회
    qna = db.query(Qna).filter(Qna.id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA를 찾을 수 없습니다.")

    # 작성자 본인만 수정 가능
    if qna.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="본인 글만 수정할 수 있습니다.")

    # 필드 업데이트
    if qna_request.title is not None:
        qna.title = qna_request.title
    if qna_request.content is not None:
        qna.content = qna_request.content

    qna.updated_at = datetime.now()  # 수정 시간 업데이트

    db.commit()
    db.refresh(qna)

    return QnaResponse.from_orm_with_label(qna)




# admin - 기존 문의글에 “답변”을 등록
@router.post("/qna/{qna_id}/answer", response_model=QnaAnswerRequest, summary='admin 1:1 문의 답글')
def create_qna_answer(
    qna_id: int,
    answer_request: QnaAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ← 로그인된 관리자
):
    #  관리자 권한 확인
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="관리자만 답변할 수 있습니다.")

    # 해당 QnA 찾기
    qna = db.query(Qna).filter(Qna.id == qna_id).first()
    if not qna:
        raise HTTPException(status_code=404, detail="QnA를 찾을 수 없습니다.")

    # 답변 등록
    qna.answer = answer_request.answer
    qna.admin_id = current_user.id  # 로그인된 관리자의 ID 저장
    qna.status = QnaStatus.answered
    qna.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(qna)

    return QnaResponse.from_orm_with_label(qna)