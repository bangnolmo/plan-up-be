# 여기는 사실 백에서 DB를 넣는 건 처음이라서 알아서 이쁘게 트리 구조를 가지면 될 듯

import sqlite3


# 데이터베이스 연결 함수
def get_connection():
    conn = sqlite3.connect(".\\app\\database\\schedule.db")
    return conn


# 테이블 생성 함수
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS lecture_schedule (
        id TEXT PRIMARY KEY,          -- 강의 ID, 텍스트 타입
        lecture_name TEXT NOT NULL,   -- 강의명
        grade INTEGER,                -- 학년
        course_type TEXT,             -- 이수 구분 (전선, 교양 등)
        credit INTEGER,               -- 학점
        professor_name TEXT,          -- 교수명
        enrollment_status TEXT,       -- 수강 상태 (수강초과 등)
        time TEXT,                    -- 강의 시간
        location TEXT                 -- 강의실 위치
    )
    """
    )
    conn.commit()
    conn.close()


def create_department_table():
    conn = get_connection()
    cursor = conn.cursor()

    # 학과 테이블 생성
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS department (
        hakgwa_cd TEXT PRIMARY KEY,   -- 학과 코드 (기본 키)
        hakgwa_name TEXT NOT NULL     -- 학과 이름
    )
    """
    )

    conn.commit()
    conn.close()


def create_department_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS department (
        hakgwa_cd TEXT PRIMARY KEY,   -- 학과 코드 (기본 키)
        hakgwa_name TEXT NOT NULL,    -- 학과 이름
        parent_cd TEXT,               -- 상위 학과 코드 (부모 학과), NULL 가능
        FOREIGN KEY (parent_cd) REFERENCES department (hakgwa_cd) -- 부모 학과 관계 설정
    )
    """
    )

    conn.commit()
    conn.close()


# 데이터 삽입 함수
def insert_lecture(
    id,
    lecture_name,
    grade,
    course_type,
    credit,
    professor_name,
    enrollment_status,
    time,
    location,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    INSERT INTO lecture_schedule (id, lecture_name, grade, course_type, credit, professor_name, enrollment_status, time, location)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            id,
            lecture_name,
            grade,
            course_type,
            credit,
            professor_name,
            enrollment_status,
            time,
            location,
        ),
    )

    conn.commit()
    conn.close()


# database.py 파일 내에서
def insert_department(hakgwa_cd, hakgwa_name, parent_cd=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO department (hakgwa_cd, hakgwa_name, parent_cd)
        VALUES (?, ?, ?)
        """,
        (hakgwa_cd, hakgwa_name, parent_cd),
    )

    conn.commit()
    conn.close()


# 데이터 조회 함수
def get_all_lectures():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lecture_schedule")

    rows = cursor.fetchall()
    conn.close()

    return rows


def check_department_exists(hakgwa_cd):
    """
    학과 코드가 데이터베이스에 존재하는지 확인하는 함수.
    :param hakgwa_cd: 학과 코드
    :return: True or False
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM department WHERE hakgwa_cd = ?", (hakgwa_cd,))
    result = cursor.fetchone()

    conn.close()

    return result is not None
