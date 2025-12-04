from __future__ import annotations
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.refresh import RefreshTokenRequest
from app.schemas.login import TokenResponse, UserInfo
from app.services.service_refresh import refresh_to_access_token

router = APIRouter()


@router.post("", response_model=TokenResponse, summary="리프레시 토큰")
def refresh_token_endpoint(request_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    refresh_token: str = request_data.refresh_token

    # 리프레시 토큰이 없는 경우
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Refresh token missing")

    # refresh token 검증 및 새 토큰 발급
    try:
        new_access_token, expires_in_seconds, user_id = refresh_to_access_token(refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e) or "Invalid or expired refresh token"
        )

    # DB에서 사용자 정보 조회
    user: User = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    print(f"새 access_token: {new_access_token}\n")

    # 액세스 토큰 반환
    return TokenResponse(
        message="토큰 재발급 성공",
        access_token=new_access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserInfo(user_id=user_id, name=user.name, role=user.role),
        expires_in=expires_in_seconds
    )
