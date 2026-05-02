import logging
from app_ezenfood.modules.utils.get_conn import get_conn
from sentence_transformers import SentenceTransformer
import json

# ─── 로거 설정 ───
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

class SubDAO:
    def __init__(self, conn_factory):
        """
        conn_factory : get_conn 같은 함수를 주입
        """
        self.conn_factory = conn_factory

    def insert(self, data_list):
        """sub_category 테이블에 데이터 삽입"""
        conn = self.conn_factory()
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO sub_category 
                (sub_name, sub_sentence, sub_sentemb, sub_keyword, sub_keyemb)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(query, data_list)
            conn.commit()
            logger.info(f"{len(data_list)}건 sub_category 테이블에 저장 완료!")
        except Exception as e:
            conn.rollback()
            logger.error("DB Insert 오류 발생", exc_info=e)
        finally:
            cursor.close()
            conn.close()

    def fetch_all(self):
        """sub_category 전체 조회"""
        conn = self.conn_factory()
        try:
            cursor = conn.cursor()
            query = """
                SELECT
                    sub_id,
                    sub_name,
                    sub_sentence,
                    sub_sentemb,
                    sub_keyword,
                    sub_keyemb
                FROM sub_category
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            logger.info(f"sub_category 조회 완료: {len(rows)}건")
            return rows
        except Exception as e:
            logger.error("DB Select 오류 발생", exc_info=e)
            return []
        finally:
            cursor.close()
            conn.close()
