import pandas as pd
from sqlalchemy import create_engine
import pymysql # PyMySQL은 SQLAlchemy의 MySQL 드라이버로 사용됨

# --- 1. 데이터베이스 연결 정보 설정 ---

db_user     = '유재욱'
db_password = 'ezen'
db_host     = '192.168.60.179'
db_name     = 'ezeneats'
table_name  = 'rest'


# --- 2. SQLAlchemy 엔진 생성 ---
# MySQL + PyMySQL 드라이버를 사용함을 명시 (mysql+pymysql)
# 문자열 형식: 'mysql+pymysql://<user>:<password>@<host>/<dbname>'
db_connection_str = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(db_connection_str)

# --- 3. DataFrame 생성 (예시) ---
df_rest    = pd.read_csv("filter_list.csv")
df_review  = pd.read_csv("reviews_repredicted.csv")
print(df_rest.info())
print(df_review.info())
print("-" * 60)
sub_category_df = pd.read_sql('SELECT sub_id, sub_name FROM sub_category', con=engine)

# --- 4. DataFrame을 MySQL 테이블로 저장 (to_sql) ---
try:
    column_mapping = {
        '상호명'     : 'rest_name',
        '경도'       : 'rest_x',
        '위도'       : 'rest_y',
        '행정동명'   : 'rest_dong',
        '도로명주소' : 'rest_addr',
        '지번주소'   : 'rest_old'
    }

    df_rest = pd.merge(
        df_rest,
        sub_category_df,
        left_on='상권업종소분류명',  # df_rest 컬럼
        right_on='sub_name', # sub_category 컬럼
        how='left'
    )
    df_rest_map = (df_rest.rename(columns=column_mapping))

    df_rest_map = df_rest_map.drop(columns=['상권업종소분류명', 'sub_name'])
    print(df_rest_map.info())
    print("-" * 60)

    df_rest_map['rest_name'] = df_rest_map['rest_name'].str.strip()
    df_review['rest_name']   = df_review['rest_name'].str.strip()

    df_review_sub = (
        df_review[['rest_name', 'nplace_id', 'review_count']]
        .drop_duplicates(subset='rest_name')
    )
    df_merged = pd.merge(
        df_rest_map,
        df_review_sub,
        on='rest_name',
        how='left' 
    )
    df_merged['nplace_id']    = df_merged['nplace_id'].fillna(0)
    df_merged['review_count'] = df_merged['review_count'].fillna(0)
    print(df_merged.info())
    df_merged.head()
    print("-" * 60)
    
    df_merged.to_sql(
        name      = table_name,
        con       = engine,
        if_exists = 'append',
        index     = False,
        chunksize = 1000
    )
    print("완b")
except Exception as e:
    print(f"오류 발생: {e}")
finally:
    # 엔진 리소스 정리 (선택 사항, 컨텍스트 관리자 사용 시 자동으로 처리될 수 있음)
    engine.dispose()
