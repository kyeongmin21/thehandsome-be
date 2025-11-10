from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.products import router as products_router
from app.api.boards import router as boards_router
from app.api.categories import router as categories_router

from app.api.auth.user import router as join_router
from app.api.auth.login import router as login_router
from app.api.auth.logout import router as logout_router
from app.api.auth.refresh import router as refresh_router

from app.api.auth.mypage import router as mypage_router

from dotenv import load_dotenv
load_dotenv()  # .env 파일 읽어서 os.environ에 반영

app = FastAPI()

# CORS 설정 (Next.js에서 호출 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # TODO: 배포 후에는 실제 프론트엔드 도메인도 추가해야 합니다.
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# 라우터 등록
app.include_router(products_router, prefix="/products", tags=["상품등록"])
app.include_router(boards_router, prefix="/boards", tags=["게시판"])
app.include_router(categories_router, prefix="/category", tags=["카테고리"])

app.include_router(join_router, prefix="/join", tags=["회원가입"])
app.include_router(login_router, prefix="/login", tags=["로그인"] )
app.include_router(logout_router, prefix="/logout", tags=["로그아웃"] )
app.include_router(refresh_router, prefix="/refresh", tags=["로그인"] )

app.include_router(mypage_router, prefix="/mypage", tags=["마이페이지"] )
