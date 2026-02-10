# import os
# import pymysql
# from dotenv import load_dotenv

# 載入 .env( 本機/Docker )
# load_dotenv()

# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_NAME = os.getenv("DB_NAME")


# def get_connection():
#     """
#     建立並回傳 MYSQL 連線
#     """
#     return pymysql.connect(
#         host=DB_HOST,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         database=DB_NAME,
#         cursorclass=pymysql.cursors.DictCursor,
#         autocommit=True,
#         port=3306,
#     )

import pymysql


def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="12345678",  # 改成你本機的
        database="bulletin_board",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
