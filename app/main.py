from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.products import router as products_router
from app.api.boards import router as boards_router
from app.api.categories import router as categories_router

app = FastAPI()

# CORS 설정 (Next.js에서 호출 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 등록
app.include_router(products_router, prefix="/products")
app.include_router(boards_router, prefix="/boards")
app.include_router(categories_router, prefix="/category")