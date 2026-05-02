import pandas as pd
from app_ezenfood import CSV_DIR
from sqlalchemy import create_engine


review_df = pd.read_csv(CSV_DIR / "reviews_repredicted.csv")


print(review_df.isna().sum())

user = "root"
password = "ezen"
localhost = "localhost"
db_name = "ezeneats"

# 2. 데이터베이스 연결 엔진 생성 (예시: SQLite)
# 'sqlite:///test_database.db'는 test_database.db라는 파일을 생성하거나 사용해요.
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{localhost}:3306/{db_name}"
)
# 3. to_sql을 사용하여 데이터 저장
try:
    review_df.to_sql(
        name='my_table',   # 저장할 테이블 이름
        con=engine,        # 연결 엔진
        if_exists='replace', # 테이블이 있으면 교체
        index=False        # 인덱스는 테이블에 컬럼으로 저장하지 않음
    )
    print("데이터 저장 성공!")
except Exception as e:
    print(f"데이터 저장 오류 발생: {e}")