from fastapi import APIRouter, HTTPException
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

# 임시 게시판 데이터 (DB 대신 리스트 사용)
boards = [
    {"id": 1, "title": "첫 글", "content": "게시판 글입니다.", "created_at": '', "x": ''},
    {"id": 2, "title": "공지사항", "content": "여기는 공지입니다.", "created_at": '', "updated_at": ''},
]

# GET
@router.get("/")
def get_boards():
    return boards


class BoardCreate(BaseModel):
    title: str
    content: str

# POST: 글 작성
@router.post("/")
def create_boards(board: BoardCreate):
    new_id = max(post["id"] for post in boards) + 1 if boards else 1
    now = datetime.now()
    new_board = {
        "id": new_id,
        "title": board.title,
        "content": board.content,
        "created_at": now.strftime("%Y-%m-%d %H:%M"),
        "updated_at": now.strftime("%Y-%m-%d %H:%M"),
    }
    boards.append(new_board)
    return {"message": "게시판 글 작성 완료", "board": new_board}



# UPDATE
@router.put("/boards/{board_id}")
def update_boards(board_id: int, title: str, content: str):
    for board in boards:
        if board["id"] == board_id:
            board["title"] = title
            board["content"] = content
            board["updated_at"] = datetime.now().isoformat()  # 수정 시간 갱신
            return board
    raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")


# DELETE: 삭제
@router.delete("/boards/{board_id}")
def delete_board(board_id: int):
    for board in boards:
        if board["id"] == board_id:
            boards.remove(board)
            return {"message": "게시판 글 삭제 완료"}
    raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")