#강의 예외 처리
class InvalidLectureException(DomainException):
    def __init__(self, message="Invalid lecture data"):
        super().__init__(message)

#학과 예외 처리
class DepartmentNotFoundException(DomainException):
    def __init__(self, hakgwa_cd, message="Department not found"):
        super().__init__(f"{message}: {hakgwa_cd}")
        