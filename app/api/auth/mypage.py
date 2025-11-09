from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from starlette import status

from app.api.auth.user import hash_password
from app.database import get_db
from app.models.user import User
from app.schemas.user import PasswordCheckResponse, PasswordCheckRequest, UserOut, UserUpdate
from app.core.security import verify_password
from app.core.security import decode_jwt_token  # JWT 토큰 디코딩 함수

router = APIRouter()

# /token 경로에서 로그인 시 토큰 발급
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 현재 로그인 사용자 가져오기
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_jwt_token(token)
        user = db.query(User).filter(User.user_id == payload.get("sub")).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/verify-password", response_model=PasswordCheckResponse,  summary="비밀번호 확인")
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
            detail="Incorrect password"
        )



# PUT (Update): 자기 정보 수정
@router.put("/{user_id}", response_model=UserOut, summary="자기 정보 수정")
def update_user(
        user_id: str,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    # 자기 정보만 수정 가능
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own account")

    db_user = db.query(User).filter(User.user_id == user_id).first()
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
