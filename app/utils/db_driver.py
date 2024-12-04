import mysql.connector

from mysql.connector import Error
from app.utils.env_util import DB_HOST
from app.utils.env_util import DB_NAME
from app.utils.env_util import DB_PASS
from app.utils.env_util import DB_USER
from app.utils.env_util import DB_PORT


def get_conn_and_cursor():
    """
    db에 연결하여 connector 과 cursort을 반환 함.
    conn, cursor = get_conn_and_cursor() 형식으로 사용하는 것을 추천 함.

    :return: [connector, cursor]
    """

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            charset="utf8",
        )
        cursor = conn.cursor()
        cursor.execute("set names utf8mb4")

        return [conn, cursor]

    except:
        raise ConnectionError("Failed to connect to database")


def close_conn_and_cursor(conn, cursor):
    """
    DB 연결을 종료 시킴

    :param conn: mysql connector
    :param cursor:  mysql cursor
    """
    cursor.close()
    conn.close()


def update_jojik_and_classes(all_jojik, all_class):
    """
    현재 학기의 조직과 과목 데이터를 받아서 업데이트 수행 함.

    :param all_jojik: 모든 조직 데이터
    :param all_class: 모든 과목 데이터
    """
    try:
        conn, cursor = get_conn_and_cursor()

        # 모든 조직 데이터 추가 하기
        sql_query = "INSERT IGNORE INTO jojik VALUES (NULL, %s, %s, %s)"

        cursor.executemany(sql_query, all_jojik)

        # 모든 수업 데이터 추가 하기
        sql_query = (
            "INSERT IGNORE INTO classes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        cursor.executemany(sql_query, all_class)

        conn.commit()

        close_conn_and_cursor(conn, cursor)

    except Error as e:
        print(f"에러 발생 : {e}")


def login_user(email, ac_token, re_token):
    """
    사용자의 정보를 추가및 업데이트

    :param email: 사용자의 이메일
    :param ac_token: 사용자의 access token
    :param re_token: 사용자의 refresh token
    :return: boolean 저장 성공 여부
    """
    try:
        conn, cursor = get_conn_and_cursor()

        # 사용자 정보 가져오기
        sql_query = "SELECT count(*) FROM users WHERE email = (%s)"
        cursor.execute(sql_query, (email,))

        res = cursor.fetchall()

        # 사용자 정보 존재 -> token 업데이트 else 사용자 등록
        if res[0][0] == 1:
            sql_query = (
                "UPDATE users SET ac_token = (%s), re_token = (%s) WHERE email = (%s)"
            )
            cursor.execute(sql_query, (ac_token, re_token, email))
        else:
            sql_query = "INSERT INTO users VALUES (%s, %s, %s)"
            cursor.execute(sql_query, (email, ac_token, re_token))

        conn.commit()

        close_conn_and_cursor(conn, cursor)

    except Error as e:
        print(f"에러 발생 : {e}")
        return False

    return True


def select_jojik_name(gubun, year, hakgi):
    """
    년도, 학기, 구분에 따른 조직 조회

    :param gubun: 구분 (1: 교양, 2: 전공)
    :param year: 검색할 년도
    :param hakgi: 검색할 학기
    :return: [{'name':str, 'idx':int}...]
    """
    try:
        conn, cursor = get_conn_and_cursor()

        find_id = year * 1000 + hakgi * 10 + gubun

        sql_query = "SELECT name, idx FROM jojik WHERE IDX % 10000000 = %s"

        cursor.execute(sql_query, (find_id,))

        data = cursor.fetchall()

        result = []
        for d in data:
            result.append({"name": d[0], "idx": d[1]})

        close_conn_and_cursor(conn, cursor)

        return result

    except Error as e:
        print(f"에러 발생 : {e}")
        return []


def select_class_by_idx(idx):
    """
    해당 구분(학과)의 개설 과목을 리턴 함.

    :param idx: 해당 학과 ID
    :return: 개설 과목들 [dict() ...]
    """
    try:
        conn, cursor = get_conn_and_cursor()

        sql_query = "SELECT * FROM classes WHERE parent_idx = %s"
        cursor.execute(sql_query, (idx,))

        data = cursor.fetchall()

        result = []
        for d in data:
            result.append(
                {
                    "sub_num": d[0],
                    "name": d[1],
                    "grade": d[2],
                    "course_type": d[3],
                    "credits": d[4],
                    "professor": d[5],
                    "note": d[6],
                    "period": d[7],
                    "location": d[8],
                    "parent_idx": d[9],
                }
            )

        close_conn_and_cursor(conn, cursor)

        return result
    except Error as e:
        print(f"에러 발생 : {e}")
        return []


def select_users_by_email(email):
    """
    email 값을 이용하여 사용자 조회함.

    :param email: 조회항 사용자
    :return: [email, ac, rc]
    """
    try:
        conn, cursor = get_conn_and_cursor()

        sql_query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql_query, (email,))

        data = cursor.fetchone()

        close_conn_and_cursor(conn, cursor)

        return data
    except Error as e:
        print(f"에러 발생 : {e}")
        return []


def update_user(email, token):
    """
    email 값을 이용하여 사용자의 ac token을 업데이트 함.

    :param token: 사용자의 access token
    :param email: 업데이트할 사용자
    :return: boolean / true : 정상, false : 비정상
    """
    try:
        conn, cursor = get_conn_and_cursor()

        sql_query = "UPDATE users SET ac_token = %s WHERE email = %s"
        cursor.execute(sql_query, (token, email))
        conn.commit()

        close_conn_and_cursor(conn, cursor)

        return True
    except Error as e:
        print(f"에러 발생 : {e}")
        return False


# Debug
def test_login_user(email, ac_token, re_token):
    return {"email": email, "ac_token": ac_token, "re_token": re_token}


def select_class_by_time_table_info(result_table):
    """
    시간표에 담긴 강의 정보 조회

    :param result_table: 시간표에 담긴 강의 정보 목록
    :return: 강의 정보
    """

    try:
        conn, cursor = get_conn_and_cursor()

        result_class = []
        for d in result_table:
            sql_query = "SELECT * FROM classes WHERE parent_idx = %s AND sub_num = %s"
            cursor.execute(sql_query, (d["class_parant_idx"], d["class_sub_num"]))

            data = cursor.fetchall()

            for d in data:
                result_class.append(
                    {
                        "sub_num": d[0],
                        "name": d[1],
                        "grade": d[2],
                        "course_type": d[3],
                        "credits": d[4],
                        "professor": d[5],
                        "note": d[6],
                        "period": d[7],
                        "location": d[8],
                        "parent_idx": d[9],
                    }
                )

        close_conn_and_cursor(conn, cursor)

        return result_class
    except Error as e:
        print(f"에러 발생 : {e}")
        return []


def create_time_table(name, year, hakgi, owner):
    """
    시간표 생성

    :param name: 시간표 명칭
    :param year: 시간표 생성 시기
    :param hakgi: 시간표 생성 학기
    :param owner: 시간표 주인
    :return: boolean / true : 성공, false : 실패
    """
    try:
        conn, cursor = get_conn_and_cursor()

        create_data = year * 100 + hakgi
        sql_query = "INSERT INTO time_table VALUES (NULL, %s, %s, %s)"

        cursor.execute(sql_query, (name, create_data, owner))
        conn.commit()

        close_conn_and_cursor(conn, cursor)

        return True

    except Error as e:
        print(f"error: {e}")
        return False


def select_time_table(email):
    """
    사용자의 시간표 조회

    :param email: 사용자 이메일
    :return: 시간표 정보
    """
    try:
        conn, cursor = get_conn_and_cursor()

        sql_query = "SELECT * FROM time_table WHERE owner = %s"
        cursor.execute(sql_query, (email,))

        data = cursor.fetchall()

        result = []
        for d in data:
            result.append(
                {"id": d[0], "name": d[1], "create_data": d[2], "owner": d[3]}
            )

        close_conn_and_cursor(conn, cursor)

        return result
    except Error as e:
        print(f"에러 발생 : {e}")
        return []


def insert_time_table_lectures(table_idx, class_idx, sub_num):
    """
    시간표에 강의 정보 삽입

    :param table_idx: 시간표 ID
    :param class_idx: 과목 idx
    :param sub_num: 수업 번호
    :return: boolean / true : 정상, false : 비정상
    """
    try:
        conn, cursor = get_conn_and_cursor()

        sql_query = "SELECT class_sub_num, class_parent_idx FROM time_table_info WHERE time_table_id = %s"
        cursor.execute(sql_query, (table_idx,))

        data = cursor.fetchall()

        for num, idx in data:
            if num == sub_num and idx == class_idx:
                return False

        sql_query = "INSERT INTO time_table_info VALUES (NULL, %s, %s, %s)"
        cursor.execute(sql_query, (table_idx, sub_num, class_idx))
        conn.commit()

        close_conn_and_cursor(conn, cursor)

        return True
    except Error as e:
        print(f"에러 발생 : {e}")
        return False


def select_class_by_time_table_idx(table_idx):
    """
    시간표에 담긴 강의 정보 조회

    :param table_idx: 시간표 ID
    :return: 시간표에 담긴 강의 정보
    """
    # table_idx로 테이브에 있는 강의 정보를 조회
    try:
        conn, cursor = get_conn_and_cursor()

        sql_query = "SELECT class_sub_num, class_parent_idx FROM time_table_info WHERE table_idx = %s"
        cursor.execute(sql_query, (table_idx,))

        data = cursor.fetchall()

        sql_query = "SELECT * FROM classes WHERE sub_num = %s and parent_idx = %s"
        cursor.executemany(sql_query, data)

        res = cursor.fetchall()

        result_table = []
        for d in res:
            result_table.append(
                {
                    "sub_num": d[0],
                    "name": d[1],
                    "grade": d[2],
                    "course_type": d[3],
                    "credits": d[4],
                    "professor": d[5],
                    "note": d[6],
                    "period": d[7],
                    "location": d[8],
                    "parent_idx": d[9],
                }
            )

        close_conn_and_cursor(conn, cursor)
        return result_table

    except Error as e:
        print(f"에러 발생 : {e}")
        return []


def delete_time_table_lectures_by_idx(table_idx, class_idx):
    """
    idx에 해당하는 테이블에 있는 과목 데이터 삭제하기

    :param table_idx: 테이블 idx
    :param class_idx: 삭제할과목의 sub_num
    :return: boolean true: 성공, false: 실패
    """
    try:
        conn, cursor = get_conn_and_cursor()

        # delete class
        sql_query = "DELETE FROM time_table_info WHERE time_table_id = %s AND class_sub_num = %s"

        cursor.execute(sql_query, (table_idx, class_idx))

        conn.commit()

        return True
    except Error as e:
        print(f"error {e}")
        return False


def delete_time_table_by_idx(table_idx):
    """
    idx에 해당하는 테이블 삭제하기

    :param table_idx:삭제할 테이블 idx
    :return: boolean true: 성공, false: 실패
    """
    try:
        conn, cursor = get_conn_and_cursor()

        # delete classes
        sql_query = "DELETE FROM time_table_info WHERE time_table_id = %s"
        cursor.execute(sql_query, (table_idx,))

        # delete table
        sql_query = "DELETE FROM time_table WHERE id = %s"
        cursor.execute(sql_query, (table_idx,))

        conn.commit()

        close_conn_and_cursor(conn, cursor)
        return True

    except Error as e:
        print(f"error : {e}")
        return False


if __name__ == "__main__":
    # print(select_users_by_email('inup@kyonggi.ac.kr'))
    # delete_time_table_lectures_by_idx(5, '0001')
    delete_time_table_by_idx(5)
    # print(create_time_table("test", 2024, 20, "inup@kyonggi.ac.kr "))

    # select_jojik_name(1, None, None)
    pass
