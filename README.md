## 🔑 인증 및 권한 (JWT 기반)

### 1️⃣ 로그인 과정
- 사용자가 아이디와 비밀번호를 입력하고 /login API를 호출합니다.
- 서버는 데이터베이스에서 해당 ID가 있는지 확인합니다.
  - 없으면 NO_ID 에러 반환
- 비밀번호를 bcrypt로 검증합니다.
  - 틀리면 INVALID_PASSWORD 에러 반환
- 검증이 성공하면 JWT 토큰 두 개를 생성합니다.
  - Access Token → API 호출 시 인증용
  - Refresh Token → Access Token이 만료됐을 때 재발급용

### 2️⃣️ Access Token 사용
- 용도: 실제 API 요청 시 사용되는 인증용 “신분증”
- 발급 위치: 로그인 API 응답(body)에 포함
- 유효 기간: 1시간 (짧음)
- 보안 특성:
  - 탈취 위험이 있지만, 짧은 만료 시간으로 피해 최소화
  - 클라이언트에서 헤더 Authorization: Bearer <access_token> 으로 요청

### 3️⃣ Refresh Token 사용
- 용도: Access Token이 만료됐을 때 새 Access Token 발급 요청
- 발급 위치: 로그인 API 응답(body)에 포함
- 유효 기간: 30일
- 클라이언트(Next-auth)에서 직접 저장 및 관리

<br/>
<br/>


## 🏗️ 아키텍처 및 코드 구성 (Layered Architecture)

본 백엔드 프로젝트는 **관심사 분리(Separation of Concerns)** 원칙을 따르는 계층형 아키텍처를 사용합니다.

* **`app/api/v1/endpoints` (Router/Controller):** 클라이언트의 HTTP 요청을 받고 응답을 반환합니다. 데이터 유효성 검사 및 서비스 계층 호출을 담당합니다.
* **`app/services` (Business Logic):** 복잡한 비즈니스 규칙과 로직을 처리합니다. 여러 CRUD 작업을 조합하거나, 데이터를 가공하는 역할을 합니다.
* **`app/crud` (Data Access Layer):** $\text{DB}$와의 직접적인 통신(Create, Read, Update, Delete)을 담당합니다. 오직 $\text{SQLAlchemy}$ 쿼리만 수행하며, 비즈니스 로직은 포함하지 않습니다.
* **`app/models` (ORM Models):** $\text{DB}$ 테이블 구조를 정의한 $\text{SQLAlchemy}$ 모델입니다.
* **`app/schemas` (Pydantic Models):** $\text{API}$ 요청(`Request Body`) 및 응답(`Response Model`)의 데이터 형식을 정의합니다.
  

<br/>
<br/>

## 💾 데이터베이스 및 ORM

* **데이터베이스:** $\text{MariaDB 11.7}$ (로컬 환경)
* **ORM (Object-Relational Mapping):** **SQLAlchemy Core & ORM**을 사용하여 데이터베이스와 상호작용합니다.
* **DB 커넥션 관리:** `app/database.py` 파일의 `get_db` 함수를 $\text{FastAPI}$의 **의존성 주입 (Dependencies)**으로 사용하여 요청당 세션을 관리하고 종료합니다.
* **DB URL 드라이버:** 호환성을 위해 **PyMySQL** 드라이버를 사용합니다. (URL 형식: `mysql+pymysql://...`)



