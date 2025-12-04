from jose import jwt
from fastapi import HTTPException
from app.core.security import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token


def refresh_to_access_token(refresh_token: str) -> str:
    """
        리프레시 토큰으로 새 액세스 토큰 생성
        - refresh_token: 클라이언트 쿠키에서 받은 리프레시 토큰
        - 반환: 새 액세스 토큰 문자열
        """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_signature": True, "verify_aud": False, "require": ["exp", "iat", "jti"]},
        )

        if payload.get("typ") != "refresh":

            raise Exception("Invalid token type")

        user_id: str = payload.get("sub")

    except jwt.ExpiredSignatureError:
        print("에러: Refresh Token 만료됨")
        raise Exception("Refresh token is expired")
    except jwt.InvalidSignatureError:
        print("에러: Refresh Token 서명 무효")
        raise Exception("Invalid refresh token signature")
    except jwt.InvalidTokenError as e:
        print(f"에러: Refresh Token 유효성 오류: {e}")
        raise Exception("Invalid refresh token")
    except Exception as e:
        print(f"에러: 알 수 없는 토큰 처리 오류: {e}")
        raise Exception("Token processing error")


    new_access_token = create_access_token(data={"sub": str(user_id)})
    expires_in_seconds = ACCESS_TOKEN_EXPIRE_MINUTES * 60

    return new_access_token, expires_in_seconds, user_id

