import mysql.connector

from mysql.connector import Error
from app.utils.env_util import DB_HOST
from app.utils.env_util import DB_NAME
from app.utils.env_util import DB_PASS
from app.utils.env_util import DB_USER
from app.utils.env_util import DB_PORT


def update_jojik_and_classes(all_jojik, all_class):
    try:
        with mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            charset='utf8'
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute("set names utf8mb4")

                # 모든 조직 데이터 추가 하기
                sql_query = "INSERT IGNORE INTO jojik VALUES (NULL, %s, %s, %s)"

                cursor.executemany(sql_query, all_jojik)

                # 모든 수업 데이터 추가 하기
                sql_query = "INSERT IGNORE INTO classes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                cursor.executemany(sql_query, all_class)

                sql_query = "SELECT * FROM jojik"

                cursor.execute(sql_query)

                data = cursor.fetchall()

                for d in data:
                    print(d)

            conn.commit()

    except Error as e:
        print(f"에러 발생 : {e}")


def select_test():
    try:
        with mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            charset='utf8'
        ) as conn:

            with conn.cursor() as cursor:
                cursor.execute("set names utf8mb4")

                sql_query = "SELECT * FROM jojik"

                cursor.execute(sql_query)

                data = cursor.fetchall()

                return data

    except Error as e:
        print(f"에러 발생 : {e}")

    return None

if __name__ == "__main__":
    update_jojik_and_classes([], [])