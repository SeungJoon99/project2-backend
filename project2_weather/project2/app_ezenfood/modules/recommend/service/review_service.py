from app_ezenfood.modules.recommend.DAO.review_dao import ReviewDAO
from app_ezenfood.modules.utils.get_conn import get_root_conn
import pandas as pd

class ReviewService:

    def __init__(self) :
        self.review_dao = ReviewDAO(get_root_conn)

    def attach_rest_id(
        self,
        review_df : pd.DataFrame
    ) -> pd.DataFrame:
        
        if 'rest_name' not in review_df.columns:
            raise ValueError("review_df에 'rest_name' 컬럼이 없습니다.")
        
        # 리뷰 DF에 rest_id 추가
        # 1. DB 음식점 정보
        rest_rows = self.review_dao.rest_id_map()
        rest_df   = pd.DataFrame(rest_rows)
        
        # 디버그 코드
        print(f"📌 음식점 수: {len(rest_df)}")
        print(f"📌 리뷰 수: {len(review_df)}")
        print(f"📌 음식점 컬럼: {list(rest_df.columns)}", flush=True)
        print(f"📌 리뷰 컬럼: {list(review_df.columns)}", flush=True)
        print("-" * 50)
        
        print(rest_df.columns)
        print("+_" * 25)
        
        merged = rest_df.copy()
        
        # 2. rest_name 기준 merge
        if 'rest_name' in review_df.columns :
            merged = review_df.merge(
                rest_df[['rest_id','rest_name']],
                on  = 'rest_name',
                how      = 'left'
            )
        if 'rest_id' not in merged.columns:
            raise RuntimeError("merge 결과에 rest_id 컬럼이 생성되지 않았습니다.")

        # 3. fallback: rest_name 기준 (rest_id 없는 행만)
        missing_mask = merged['rest_id'].isna()

        # 4. 매핑 결과 요약 출력
        success_cnt = merged['rest_id'].notna().sum()
        fail_cnt = merged['rest_id'].isna().sum()

        print(f"✅ 매핑 성공: {success_cnt}")
        print(f"❌ 매핑 실패: {fail_cnt}")

        return merged
