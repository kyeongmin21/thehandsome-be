from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(500))
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.now,onupdate=datetime.now)

