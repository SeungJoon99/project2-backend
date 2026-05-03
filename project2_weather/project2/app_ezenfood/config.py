import os
class DBConfig:
    HOST = os.environ.get('DB_HOST', '127.0.0.1')
    PORT = int(os.environ.get('DB_PORT', 3306))
    USER = os.environ.get('DB_USER', 'root')
    PASSWORD = os.environ.get('DB_PASSWORD', 'ezen')
    NAME = os.environ.get('DB_NAME', 'whateatnow')