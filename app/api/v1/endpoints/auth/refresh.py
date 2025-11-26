from __future__ import annotations
from typing import Optional
from fastapi import Cookie, APIRouter, Response
from app.services.service_refresh import refresh_to_access_token
from app.schemas.login import TokenResponse, UserInfo

router = APIRouter()


@router.post("", response_model=TokenResponse, summary="리프레시 토큰")
def refresh_token_endpoint(response: Response, refresh_token: Optional[str] = Cookie(None)):
    new_access_token, new_refresh_token, user_id = refresh_to_access_token(refresh_token)

    # 새 refresh_token을 쿠키로 설정 (클라이언트 브라우저 갱신)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7일
    )

    return TokenResponse(
        message="토큰 재발급 성공",
        access_token=new_access_token,
        token_type="bearer",
        user=UserInfo(user_id=user_id)
    )
