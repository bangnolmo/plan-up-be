import mysql.connector

from mysql.connector import Error
from starlette.responses import JSONResponse
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
            charset='utf8'
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
        sql_query = "INSERT IGNORE INTO classes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

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
        cursor.execute(sql_query, (email, ))

        res = cursor.fetchall()

        # 사용자 정보 존재 -> token 업데이트 else 사용자 등록
        if res[0][0] == 1:
            sql_query = "UPDATE users SET ac_token = (%s), re_token = (%s) WHERE email = (%s)"
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
    try:
        conn, cursor = get_conn_and_cursor()

        find_id = year * 1000 + hakgi * 10 + gubun

        sql_query = "SELECT name, idx FROM jojik WHERE IDX % 10000000 = %s"

        cursor.execute(sql_query, (find_id, ))

        data = cursor.fetchall()


        result = []
        for d in data:
            result.append({
                'name': d[0],
                'idx': d[1]
            })

        close_conn_and_cursor(conn, cursor)

        return result

    except Error as e:
        print(f"에러 발생 : {e}")
        return []

    if id == "1":
        return JSONResponse(status_code=200, content=[{
                "name": "수원주간·00.교내이러닝",
                "idx": 12024201
        },
        {
                "name": "수원주간·01.가상대학이러닝",
                "idx": 22024201
        }])

    elif id == "2":
        return JSONResponse(status_code=200, content=[{
            "name": "수원주간-대학-예술체육대학-디자인비즈학부-시각정보디자인전공",
            "idx": 32024201
        },
        {
            "name": "수원주간-대학-예술체육대학-디자인비즈학부-산업디자인전공",
            "idx": 42024201
        }])
    else:
        return JSONResponse(status_code=404, content={"message": "Data not found"})
        
def select_class_by_idx(idx):
    # try:
    #     conn, cursor = get_conn_and_cursor()

    #     sql_query = "SELECT * FROM classes WHERE parent_idx = %s"

    #     cursor.execute(sql_query)

    #     data = cursor.fetchall()

    #     close_conn_and_cursor(conn, cursor)

    #     return data

    # except Error as e:
    #     print(f"에러 발생 : {e}")

    return JSONResponse(status_code=200, content=[{
        "sub_num": "85511",
        "name": "창의기초설계",
        "grade": "1",
        "course_type": "컴터",
        "credits": "3",
        "professor": "이동훈",
        "note": "",
        "period": "화 1 2 3",
        "location": "7509 10PC실",
        "parent_idx":"12024201"
    }])


if __name__ == "__main__":
    select_jojik_name(1, 2024, 20)