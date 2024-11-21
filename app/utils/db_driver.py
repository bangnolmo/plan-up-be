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


def select_test():
    try:
        conn, cursor = get_conn_and_cursor()

        sql_query = "SELECT * FROM jojik"

        cursor.execute(sql_query)

        data = cursor.fetchall()

        close_conn_and_cursor(conn, cursor)

        return len(data)

    except Error as e:
        print(f"에러 발생 : {e}")
        
    return None

def select_jojik_name(id, year, hakgi):
    # try:
    #     conn, cursor = get_conn_and_cursor()

    #     sql_query = "SELECT name,idx FROM jojik WHERE id = %s AND FLOOR((idx%10000000)/1000)= %s AND FLOOR((idx%1000)/10) = %s"

    #     cursor.execute(sql_query, (id, year, hakgi))

    #     data = cursor.fetchone()

    #     close_conn_and_cursor(conn, cursor)

    #     return data

    # except Error as e:
    #     print(f"에러 발생 : {e}")
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
        "id": "85511",
        "year": "1170",
        "name": "창설",
        "grade": "1",
        "course_type": "컴터",
        "credit": "3",
        "professor_name": "이동훈",
        "enrollment_status": "",
        "time": "화 1 2 3",
        "location": "7509 10PC실"
    }])


if __name__ == "__main__":
    update_jojik_and_classes([], [])