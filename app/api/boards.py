from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import datetime

from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate, BoardOut

router = APIRouter()


# GET: 모든 게시글 조회
@router.get("", response_model=list[BoardOut])
def get_boards(db: Session = Depends(get_db)):
    return db.query(Board).all()


# GET: 단일 게시글 조회
@router.get("/{board_id}", response_model=BoardOut)
def get_board(board_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")
    return board


# POST: 게시글 작성
@router.post("", response_model=BoardOut)
def create_board(board: BoardCreate, db: Session = Depends(get_db)):
    new_board = Board(
        title=board.title,
        content=board.content,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board


# PUT: 게시글 수정
@router.put("/{board_id}", response_model=BoardOut)
def update_board(board_id: int, update: BoardUpdate, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")
    board.title = update.title
    board.content = update.content
    board.updated_at = datetime.now()
    db.commit()
    db.refresh(board)
    return board


# DELETE: 게시글 삭제
@router.delete("/{board_id}")
def delete_board(board_id: int, db: Session = Depends(get_db)):
    board = db.query(Board).filter(Board.id == board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="글을 찾을 수 없습니다.")
    db.delete(board)
    db.commit()
    return {"message": "게시판 글 삭제 완료"}
