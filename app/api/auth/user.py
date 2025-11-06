from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from app.database import get_db
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate, UserOut

router = APIRouter()

# 비밀번호 해싱 함수 정의
pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__ident="2b",
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.get("", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# POST: 사용자 생성
@router.post("", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    errors = []

    # 중복 체크
    if db.query(User).filter(User.user_id == user.user_id).first():
        errors.append({"field": "user_id", "code": "USER_ID_TAKEN"})
    if db.query(User).filter(User.email == user.email).first():
        errors.append({"field": "email", "code": "EMAIL_TAKEN"})
    if db.query(User).filter(User.phone == user.phone).first():
        errors.append({"field": "phone", "code": "PHONE_TAKEN"})

    # 에러 있으면 리스트로 반환
    if errors:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": errors}
        )

    hashed_pw = hash_password(user.password)

    new_user = User(
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        password=hashed_pw,
        phone=user.phone,
        role=user.role,
        login_type=user.login_type,
        membership_grade=user.membership_grade
    )

    db.add(new_user)
    db.commit() # DB에 변경사항 반영 (저장)
    db.refresh(new_user)
    return new_user



