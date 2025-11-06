from __future__ import annotations
from typing import Optional
from fastapi import HTTPException, Cookie, APIRouter
from jose import JWTError, jwt
from app.core.security import SECRET_KEY, ALGORITHM, create_access_token
from app.schemas.login import TokenResponse, UserInfo

router = APIRouter()


@router.post("", response_model=TokenResponse)
def refresh_token_endpoint(refresh_token: Optional[str] = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("typ") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token(data={"sub": str(user_id)})

    return TokenResponse(
        message="토큰 재발급 성공",
        access_token=new_access_token,
        token_type="bearer",
        user=UserInfo(user_id=user_id)
    )
