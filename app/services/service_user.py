from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.crud.crud_user import create_user as crud_create_user

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__ident="2b", deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def register_user(db: Session, user: UserCreate, client_ci: str) -> User:
    hashed_pw = hash_password(user.password)
    new_user = User(
        ci=client_ci,
        user_id=user.user_id,
        name=user.name,
        email=user.email,
        password=hashed_pw,
        phone=user.phone,
        role=user.role,
        login_type=user.login_type,
        membership_grade=user.membership_grade,
        address=user.address,
        marketing_agree=user.marketing_agree,
        birth_date=user.birth_date
    )
    return crud_create_user(db, new_user)
