# 인증 및 권한 (JWT 기반)

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
- 발급 위치: HttpOnly 쿠키에 담겨서 클라이언트 전달
- 유효 기간: 30일
- 보안 특성:
  - JS에서 접근 불가 → XSS 공격 방어
  - CSRF 방어에 도움 (samesite="lax")

정리하면 <br>
Access Token → 짧은 기간, API 요청용, 탈취 피해 최소화 <br>
Refresh Token → 긴 기간, 쿠키에 안전하게 저장, Access Token 재발급용




