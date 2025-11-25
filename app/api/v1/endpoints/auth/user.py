from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.crud.crud_user import create_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.dependencies.auth_deps import generate_ci

router = APIRouter()

@router.get("", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


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

    client_ci = generate_ci()
    new_user = create_user(db, user, client_ci)
    return new_user