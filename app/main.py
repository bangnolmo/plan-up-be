# main.py 파일

from database import create_table, get_all_lectures

# 1. 테이블 생성
create_table()

# 3. 데이터 조회
schedules = get_all_lectures()

# 조회한 데이터를 출력
for schedule in schedules:
    print(
        f"ID: {schedule[0]}, 강의명: {schedule[1]}, 교수명: {schedule[2]}, 시간: {schedule[3]}, 장소: {schedule[4]}"
    )
