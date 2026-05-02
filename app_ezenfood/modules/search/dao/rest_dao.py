import pandas as pd
import logging
import math

# ─── 로거 설정 ───
logger = logging.getLogger(__name__)
# __name__을 사용하면 현재 모듈 이름이 로거 이름이 됨
logger.setLevel(logging.INFO)
# 최소 레벨은 INFO부터
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# 출력 형식 설정 = 로그가 기록된 시간 - 로그 레벨 - 실제 메세지

# 콘솔 핸들러
# 핸들러(handler): 로그를 어디로 보낼지 지정하는 객체
ch = logging.StreamHandler()
# StreamHandler → 콘솔(stdout)로 출력
# FileHandler → 파일로 출력 가능
ch.setFormatter(formatter)
# 출력 형식 지정
logger.addHandler(ch)
# 로거에 핸들러 연결

# ─── DAO 클래스 ───
class RestDAO :
    def __init__(self, conn_factory) :
        self.conn_factory = conn_factory

    def insert(self, df: pd.DataFrame) :
        conn = self.conn_factory()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT sub_id, sub_name FROM sub_category")
            sub_rows = cursor.fetchall()
            sub_dict = {row['sub_name']: row['sub_id'] for row in sub_rows}

            # NaN값 > None으로 변환 (None은 mysql이 null로 처리 가능)
            def nan_to_none(v):
                if pd.isna(v):
                    return None
                if isinstance(v, float) and (math.isinf(v)):
                    return None
                return v
            
            data_to_insert = []
            for _, row in df.iterrows() :
                sub_name = row["상권업종소분류명"]
                sub_id   = sub_dict.get(sub_name)

                if sub_id is not None :
                    data_to_insert.append((
                        row["상호명"],
                        sub_id,
                        row["행정동명"],
                        row["지번주소"],
                        row["도로명주소"],
                        row["경도"],
                        row["위도"],
                        nan_to_none(row["review_count"]),
                        nan_to_none(row["nplace_id"])
                    ))
                else :
                    logger.warning(f"소분류 '{sub_name}'에 해당하는 ID가 없습니다. 건너뜀.")

            insert_query = """
                INSERT INTO rest
                (rest_name, sub_id, rest_dong, rest_old, rest_addr, rest_x, rest_y, review_count, nplace_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, data_to_insert)
            conn.commit()
            logger.info(f"CSV 데이터 {len(data_to_insert)}건 rest 테이블에 저장 완료!")
        except Exception as e :
            conn.rollback()
            logger.error("DB 오류 발생", exc_info=e)
        finally :
            cursor.close()
            conn.close()

    def select_by_sub(self, sub_id=None) :
        conn = self.conn_factory()
        try:
            cursor = conn.cursor()
            if sub_id :
                sql = "SELECT * FROM rest WHERE sub_id=%s"
                cursor.execute(sql, (sub_id,))
            else :
                sql = "SELECT * FROM rest"
                cursor.execute(sql)
            rows = cursor.fetchall()
            logger.info(f"rest 조회 완료: {len(rows)}건")
            return rows
        except Exception as e :
            logger.error("DB Select 오류", exc_info=e)
            return []
        finally :
            cursor.close()
            conn.close()
