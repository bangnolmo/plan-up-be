class LectureEntity:
    
    #초기화
    def __init__(self, id, lecture_name, grade, course_type, credit, professor_name, enrollment_status, time, location):
        self.id = id
        self.lecture_name = lecture_name
        self.grade = grade
        self.course_type = course_type
        self.credit = credit
        self.professor_name = professor_name
        self.enrollment_status = enrollment_status
        self.time = time
        self.location = location

    #유효성 검사
    def is_valid(self):
        if not self.id or not self.lecture_name:
            return False
        return True
    
    #__dict__ 반환
    def to_dict(self):
        return vars(self)