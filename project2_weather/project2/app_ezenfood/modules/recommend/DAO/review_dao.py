import pandas as pd

class ReviewDAO:

    def __init__(self, conn_factory) :
        self.conn_factory = conn_factory

    # db의 음식점과 review.csv 매핑에 사용 할 음식점 정보 조회
    def rest_id_map(self) :
        conn = self.conn_factory()
        try :
            # 실행 후 {}로 반환
            cursor = conn.cursor()
            cursor.execute("""
                SELECT rest_id, rest_name, nplace_id
                FROM rest
            """)
            rows = cursor.fetchall()
            
            print("+_" * 25)
            print(len(rows))
            print("==" * 25)
            print(rows, type(rows), "321")
            
            return rows
        except Exception as e :
            print("rest select 중 오류 발생 :", e)
            raise
        finally :
            cursor.close()
            conn.close()

    # 파라미터df = 리뷰df + rest_id + nplace_id
    def insert_reviews(self, df: pd.DataFrame):
        conn = self.conn_factory()
        print("==" * 25)
        print(df[['rest_id']].isna().sum())
        print(df[df['rest_id'].isna()].head())
        print("+_" * 25)
        try :
            cursor = conn.cursor()
            sql = """
                INSERT INTO review (
                    rest_id,
                    review_content,
                    review_wdate,
                    review_tokens,
                    review_emotion,
                    review_prob
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            # INSERT IGNORE INTO : 중복삽입 방지
            print(df.info())
            
            data = [
                (
                    int(row['rest_id']),
                    row['review_content'],
                    row['review_wdate'],
                    row.get('review_tokens'),
                    row['review_emotion'],
                    row.get('review_prob')
                )
                for _, row in df.iterrows()
            ]

            cursor.executemany(sql, data)
            conn.commit()
        except Exception as e :
            conn.rollback()
            print("review insert 중 오류 발생 :", e)
            raise
        finally :
            cursor.close()
            conn.close()