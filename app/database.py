import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path


# DB 파일 자체에서 환경 변수를 로드합니다.
# .env 파일 위치를 기준으로 경로를 명시합니다.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


# MySQL 연결 정보
# MYSQL_USER = "fastapi_user"
# MYSQL_PASSWORD = "1204"
# MYSQL_HOST = "localhost"
# MYSQL_PORT = "3306"
# MYSQL_DB = "thehandsome"

# Railway 환경변수 가져오기
DB_USER = os.getenv("PGUSER")
DB_PASSWORD = os.getenv("PGPASSWORD")
DB_HOST = os.getenv("PGHOST")
DB_PORT = os.getenv("PGPORT")
DB_NAME = os.getenv("PGDATABASE")


# SQLAlchemy 데이터베이스 URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# SQLAlchemy 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Psycopg의 타입 처리를 초기화하고 SQLAlchemy가 PG 타입을 더 잘 인식하도록 돕는 옵션
    connect_args={
        "options": "-c application_name=my_app",
        "autocommit": False,
    },
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
