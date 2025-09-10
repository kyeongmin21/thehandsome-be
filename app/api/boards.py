from fastapi import APIRouter, HTTPException
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

# 임시 게시판 데이터 (DB 대신 리스트 사용)
boards = [
    {"id": 1, "title": "첫 글", "content": "게시판 글입니다.", "created_at": '', "x": ''},
    {"id": 2, "title": "공지사항", "content": "여기는 공지입니다.", "created_at": '', "updated_at": ''},
    {"id": 3, "title": "공지사항", "content": "여기는 공지입니다.", "created_at": '', "updated_at": ''},
]

# GET
@router.get("")
def get_boards():
    return boards


# GET: 단일 글 조회
@router.get("/{board_id}")
def get_board(board_id: int):
    for board in boards:
        if board["id"] == board_id:
            return board
    raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")


# POST: 글 작성
class BoardCreate(BaseModel):
    title: str
    content: str

@router.post("/create")
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
class BoardUpdate(BaseModel):
    title: str
    content: str

@router.put("/edit/{board_id}")
def update_boards(board_id: int, update: BoardUpdate):
    now = datetime.now()
    for board in boards:
        if board["id"] == board_id:
            board["title"] = update.title
            board["content"] = update.content
            board["updated_at"] = now.strftime("%Y-%m-%d %H:%M")
            return board
    raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")


# DELETE: 삭제
@router.delete("/{board_id}")
def delete_board(board_id: int):
    for board in boards:
        if board["id"] == board_id:
            boards.remove(board)
            return {"message": "게시판 글 삭제 완료"}
    raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")