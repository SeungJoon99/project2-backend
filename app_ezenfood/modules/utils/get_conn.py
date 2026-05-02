import pymysql

def get_conn() :
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="ezen",
        database="whateatnow",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

def get_root_conn() :
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="ezen",
        database="whateatnow",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    
def get_user_conn() :
    return pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="ezen",
        database="whateatnow",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )