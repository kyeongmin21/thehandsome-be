import secrets

def generate_ci(length: int = 10) -> str:
    """
    안전한 랜덤 10자리 문자열 생성
    - 16진수 기반 (0-9, a-f)
    - ex: '03ceccb055'
    """
    return secrets.token_hex(length // 2)