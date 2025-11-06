from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.products import router as products_router
from app.api.boards import router as boards_router
from app.api.categories import router as categories_router
from app.api.user import router as user_router

app = FastAPI()

# CORS 설정 (Next.js에서 호출 가능하게)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",  # 개발 환경
        "http://localhost:3000",  # 개발 환경
        "http://127.0.0.1:3000",
        # TODO: 배포 후에는 실제 프론트엔드 도메인도 추가해야 합니다.
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 등록
app.include_router(products_router, prefix="/products")
app.include_router(boards_router, prefix="/boards")
app.include_router(categories_router, prefix="/category")
app.include_router(user_router, prefix="/user")