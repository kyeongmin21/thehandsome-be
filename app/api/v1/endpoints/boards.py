from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.crud_board import get_boards, get_board_by_id, create_board
from app.database import get_db
from app.schemas.board import BoardCreate, BoardUpdate, BoardOut

router = APIRouter()


# GET: 모든 게시글 조회
@router.get("", response_model=list[BoardOut])
def get_boards(db: Session = Depends(get_db)):
    return get_boards(db)


# GET: 단일 게시글 조회
@router.get("/{board_id}", response_model=BoardOut)
def get_board(board_id: int, db: Session = Depends(get_db)):
    board = get_board_by_id(db, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")
    return board


# POST: 게시글 작성
@router.post("", response_model=BoardOut)
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    return create_board(db, board.title, board.content)


# PUT: 게시글 수정
@router.put("/{board_id}", response_model=BoardOut)
def update_board(board_id: int, update: BoardUpdate, db: Session = Depends(get_db)):
    board = get_board_by_id(db, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")
    return update_board(db, board, update.title, update.content)


# DELETE: 게시글 삭제
@router.delete("/{board_id}")
def delete_board(board_id: int, db: Session = Depends(get_db)):
    board = get_board_by_id(db, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")
    db.delete(board)
    db.commit()
    return {"message": "게시판 글 삭제 완료"}
