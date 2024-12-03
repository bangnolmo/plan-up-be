#토큰 만료 예외 처리
class TokenExpiredException(Exception):
    def __init__(self, message="Token expired"):
        super().__init__(message)

#토큰 에러 예외 처리
class InvaildTokenException(Exception):
    def __init__(self, message="Invalid token"):
        super().__init__(message)