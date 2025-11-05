from enum import Enum as PyEnum

# 로그인 타입을 정의하는 Enum
class UserLoginType(PyEnum):
    GENERAL = "general"
    KAKAO = "kakao"
    # 필요하다면 다른 로그인 타입도 추가

# 나머지 import는 그대로 둡니다.
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime