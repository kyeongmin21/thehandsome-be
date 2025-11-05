from pydantic import BaseModel
from datetime import datetime

# 글 작성할 때 프론트에서 보내는 입력용 데이터 (프론트 > 백엔드)
class BoardCreate(BaseModel):
    title: str
    content: str

# 글 수정할 때 프론트에서 보내는 입력용 데이터 (Create와 거의 동일하지만, 목적 구분)
class BoardUpdate(BaseModel):
    title: str
    content: str

# DB에서 가져온 데이터를 프론트로 내려줄 때 쓰는 출력용 데이터
class BoardOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M")  # 원하는 포맷
        }
