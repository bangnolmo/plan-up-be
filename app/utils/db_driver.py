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


def update_user(email, ac_token, re_token):
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


if __name__ == "__main__":
    update_jojik_and_classes([], [])