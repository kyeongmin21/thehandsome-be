from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.board import Board


def get_boards(db: Session) -> List[Board]:
    return db.query(Board).all()


def get_board_by_id(db: Session, board_id: int) -> Optional[Board]:
    return db.query(Board).filter(Board.id == board_id).first()


def create_board(db: Session, title: str, content: str) -> Board:
    from datetime import datetime
    new_board = Board(
        title=title,
        content=content,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    return new_board


def update_board(db: Session, board: Board, title: str, content: str) -> Board:
    from datetime import datetime
    board.title = title
    board.content = content
    board.updated_at = datetime.now()
    db.commit()
    db.refresh(board)
    return board


def delete_board(db: Session, board: Board):
    db.delete(board)
    db.commit()
