from app.domain.entities.lecture import Lecture
import app.database.database as db
from app.domain.exceptions.exceptions import InvalidLectureException

#ID로 검색
def get_lecture_by_id(lecture_id):

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lecture_schedule WHERE id = ?", (lecture_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise InvalidLectureException(f"Lecture with ID {lecture_id} not found.")
    
    lecture = Lecture(*row)
    return lecture.to_dict()

#모든 강의 정보 출력
def get_all_lectures():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lecture_schedule")
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cursor.fetchall()
    conn.close()

    lectures = [Lecture(*row) for row in rows]
    return lectures

if __name__ == "__main__":
    db.create_table()