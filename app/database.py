# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# MySQL 연결 정보
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

# SQLAlchemy 데이터베이스 URL
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# SQLAlchemy 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,   # 실행되는 SQL 로그 출력 (개발용)
    future=True  # SQLAlchemy 2.0 스타일
)

# 세션 생성기
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base 클래스: 모델 정의 시 상속
Base = declarative_base()

# FastAPI에서 DB 세션 가져오기
def get_db():
    """
    Dependency로 사용:
    요청마다 새로운 DB 세션을 생성하고 사용 후 종료
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
