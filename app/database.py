# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 연결 정보
MYSQL_USER = "fastapi_user"
MYSQL_PASSWORD = "1204"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "thehandsome"

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
