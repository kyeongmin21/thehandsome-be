from __future__ import annotations
from typing import Optional
from fastapi import Cookie, APIRouter
from app.services.service_refresh import refresh_to_access_token
from app.schemas.login import TokenResponse, UserInfo

router = APIRouter()


@router.post("", response_model=TokenResponse, summary="리프레시 토큰")
def refresh_token_endpoint(refresh_token: Optional[str] = Cookie(None)):
    new_access_token, user_id = refresh_to_access_token(refresh_token)

    return TokenResponse(
        message="토큰 재발급 성공",
        access_token=new_access_token,
        token_type="bearer",
        user=UserInfo(user_id=user_id)
    )
