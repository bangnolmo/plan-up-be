#기본 예외 처리
class DomainException(Exception):
    def __init__(self, message="An error occurred in the domain"):
        super().__init__(message)

#강의 예외 처리
class InvalidLectureException(DomainException):
    def __init__(self, message="Invalid lecture data"):
        super().__init__(message)

#학과 예외 처리
class DepartmentNotFoundException(DomainException):
    def __init__(self, hakgwa_id, message="Department not found"):
        super().__init__(f"{message}: {hakgwa_id}")
        
#유저 예외 처리
class UserNotFoundException(DomainException):
    def __init__(self, user_email, message="User not found"):
        super().__init__(f"{message}: {user_email}")   

#시간표 예외 처리
class TimetableNotFoundException(DomainException):
    def __init__(self, table_id, message="Timetable not found"):
        super().__init__(f"{message}: {table_id}")

#시간표 생성 예외 처리
class TimetableCreationException(DomainException):
    def __init__(self, message="Timetable creation failed"):
        super().__init__(message)

#로그인 실패 예외 처리
class LoginException(DomainException):
    def __init__(self, message="Login failed"):
        super().__init__(message)

#잘못된 데이터 형식 예외 처리
class InvalidDataFormatException(DomainException):
    def __init__(self, message="Invalid data format"):
        super().__init__(message)