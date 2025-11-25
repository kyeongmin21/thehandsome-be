from fastapi import APIRouter, Response

router = APIRouter()


@router.post("", summary="로그아웃")
def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")

    return {"message": "로그아웃 성공"}