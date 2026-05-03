import pymysql
from config import DBConfig

def get_conn() :
    return pymysql.connect(
        host=DBConfig.HOST,
        user=DBConfig.USER,
        password=DBConfig.PASSWORD,
        database=DBConfig.NAME,
        port=DBConfig.PORT,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def get_root_conn() :
    return pymysql.connect(
        host=DBConfig.HOST,
        user=DBConfig.USER,
        password=DBConfig.PASSWORD,
        database=DBConfig.NAME,
        port=DBConfig.PORT,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    
def get_user_conn() :
    return pymysql.connect(
        host=DBConfig.HOST,
        user=DBConfig.USER,
        password=DBConfig.PASSWORD,
        database=DBConfig.NAME,
        port=DBConfig.PORT,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )