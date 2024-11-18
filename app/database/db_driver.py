import mysql.connector

from mysql.connector import Error
from app.utils.env_util import DB_HOST
from app.utils.env_util import DB_NAME
from app.utils.env_util import DB_PASS
from app.utils.env_util import DB_USER


def update_jojik_and_classes(all_jojik, all_class):
    try:
        with mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        ) as conn:

            with conn.cursor() as cursor:

                # 모든 조직 데이터 추가 하기
                sql_query = "INSERT IGNORE INTO jojik VALUES (NULL, %s, %s, %s)"

                cursor.executemany(sql_query, all_jojik)

                # 모든 수업 데이터 추가 하기


            conn.commit()

    except Error as e:
        print(f"에러 발생 : {e}")

