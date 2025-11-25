from jose import JWTError, jwt
from fastapi import HTTPException
from app.core.security import SECRET_KEY, ALGORITHM, create_access_token


def refresh_to_access_token(refresh_token: str) -> str:
    """
        리프레시 토큰으로 새 액세스 토큰 생성
        - refresh_token: 클라이언트 쿠키에서 받은 리프레시 토큰
        - 반환: 새 액세스 토큰 문자열
        """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("typ") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token missing user info")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # 새 액세스 토큰 생성
    new_access_token = create_access_token(data={"sub": str(user_id)})
    return new_access_token, user_id

