from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.products import router as products_router
from app.api.v1.endpoints.boards import router as boards_router
from app.api.v1.endpoints.categories import router as categories_router

from app.api.v1.endpoints.auth.user import router as join_router
from app.api.v1.endpoints.auth.login import router as login_router
from app.api.v1.endpoints.auth.logout import router as logout_router
from app.api.v1.endpoints.auth.refresh import router as refresh_router
from app.api.v1.endpoints.auth.find import router as find_router

from app.api.v1.endpoints.auth.mypage import router as mypage_router
from app.api.v1.endpoints.qna import router as qna_router

from app.api.v1.endpoints.wishlist import router as wishlist_router
from app.api.v1.endpoints.brandlike import router as brandlike_router
from app.api.v1.endpoints.brands import router as brands_router


from dotenv import load_dotenv
load_dotenv()  # .env 파일 읽어서 os.environ에 반영

app = FastAPI(title='thehansome-project', description='API documentation', version='1.0.0')


# 1. Middleware 등록 (무조건 라우터 등록 전에!)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000", # TODO: 배포 후에는 실제 프론트엔드 도메인도 추가해야 합니다.
    "https://thehandsome-fe.vercel.app"
]

# CORS 설정 (Next.js에서 호출 가능하게)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 개발용
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
app.include_router(find_router, prefix="/find", tags=["찾기"] )

app.include_router(mypage_router, prefix="/mypage", tags=["마이페이지"] )
app.include_router(qna_router, prefix="/mypage", tags=["마이페이지 - 1:1 문의"] )

app.include_router(wishlist_router, prefix="/wishlist", tags=["위시리스트"] )
app.include_router(brandlike_router, prefix="/brandlike", tags=["좋아요 브랜드"] )
app.include_router(brands_router, prefix="/brands", tags=["브랜드 리스트"] )
