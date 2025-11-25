from pydantic import BaseModel, EmailStr


# 요청 DTO
class FindIdRequest(BaseModel):
    email: EmailStr  # 이메일로 아이디 찾기


# 응답 DTO
class FindIdResponse(BaseModel):
    user_id: str
