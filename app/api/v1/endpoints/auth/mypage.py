from starlette import status
from datetime import datetime
from sqlalchemy.orm.session import Session
from fastapi import Depends, APIRouter, HTTPException, Response, Request

from app.crud.crud_user import get_user_by_id
from app.dependencies.auth_deps import get_current_user
from app.services.service_user import hash_password
from app.database import get_db
from app.models.user import User
from app.schemas.user import PasswordCheckResponse, PasswordCheckRequest, UserOut, UserUpdate
from app.core.security import verify_password

router = APIRouter()


# 내 정보 조회
@router.get("/me", response_model=UserOut, summary="내 정보 조회")
def get_my_info(current_user: User = Depends(get_current_user)):
    return current_user


# 마이페이지 : 개인정보 변경시 본인 확인용
@router.post("/verify-password",
             response_model=PasswordCheckResponse,
             summary="개인정보 변경시 본인 확인용")
def verify_user_password(
        req: PasswordCheckRequest,
        current_user: User = Depends(get_current_user)
):
    if verify_password(req.password, current_user.password):
        # 비밀번호 일치: 200 OK와 함께 verified=True 반환
        return PasswordCheckResponse(verified=True)
    else:
        # 비밀번호 불일치: 401 Unauthorized 에러 발생
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"field": "password", "code": "INVALID_PASSWORD"}]
        )


# PUT (Update): 자기 정보 수정
@router.put("/me", response_model=UserOut, summary="자기 정보 수정")
def update_user(
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_user = get_user_by_id(db, current_user.user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 비밀번호 변경 요청이 있을 경우만 해싱
    if user_update.password:
        db_user.password = hash_password(user_update.password)

    # 나머지 필드 업데이트
    for field, value in user_update.model_dump(exclude_unset=True).items():
        if field != "password":
            setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# DELETE 탈퇴하기 : 비활성처리
@router.delete("/me",
               status_code=status.HTTP_200_OK,
               summary="회원 탈퇴(is_active 비활성화)")
def deactivate_user(
        response: Response,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_user = get_user_by_id(db, current_user.user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.is_active = False
    db_user.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(db_user)

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"detail": "User deactivated successfully"}
