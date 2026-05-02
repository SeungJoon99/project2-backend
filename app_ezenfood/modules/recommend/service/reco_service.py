import pandas as pd

from app_ezenfood.modules.recommend.DAO.reco_dao import RecommendDAO
from app_ezenfood.modules.utils.get_conn import get_user_conn
from app_ezenfood.modules.recommend.engine.reco_rest import RestaurantRecommendationEngine

class RestaurantRecommendService :

    def __init__(self, alpha: int = 5, beta: int = 5) :
        # 베이지안 사전 분포 (중립 0.5 기준)
        # 결측값, 미달값을 0.5로 두고 긍/부 점수 계산
        self.alpha    = alpha
        self.beta     = beta
        self.reco_dao = RecommendDAO(get_user_conn)
        self.engine   = RestaurantRecommendationEngine()

    # 리뷰기반 추천도 계산 메서드
    def _calculate_positive_ratio(
        self,
        rest_df   : pd.DataFrame,
        review_df : pd.DataFrame
    ) -> pd.DataFrame:
        
        df = rest_df.copy()

        # 1. 리뷰 집계 (rest_id 기준)
        review_stat = (
            review_df
            .groupby('rest_id')
            .agg(
                positive_reviews=('review_emotion', lambda x: (x == 1).sum()),
                total_reviews=('review_emotion', 'count')
            )
            .reset_index()
        )

        # 2. 음식점 DF에 merge
        df = df.merge(review_stat, on='rest_id', how='left')

        # 3. 리뷰 없음 처리
        df['positive_reviews'] = df['positive_reviews'].fillna(0)
        df['total_reviews']    = df['total_reviews'].fillna(0)

        # 4. 베이지안 긍정 비율 계산
        df['positive_ratio']   = (
            (df['positive_reviews'] + self.alpha) /
            (df['total_reviews'] + self.alpha + self.beta)
        )

        return df
    
    # 음식점 추천 로직 top_n 개수만큼 반환
    def recommend_restaurants(
        self,
        sub_id          : int,
        user_lat        : float,
        user_lon        : float,
        max_distance_km : float = 1.0,
        top_n           : int = 5
    ) -> pd.DataFrame:
        
        # 음식점 추천 전체 흐름
        # 1. 음식점 + 리뷰 집계 데이터
        rest_df   = self.reco_dao.fetch_rest_list(sub_id)
        
        # sub_id에 해당하는 음식점이 없을 때
        if rest_df.empty :
            return pd.DataFrame()
            #raise ValueError("해당 카테고리에 음식점이 없습니다.")

        #print(rest_df.head(10))
        #print(rest_df.info())
        review_df = self.reco_dao.fetch_reviews()
        #print("++" * 25)

        # 2. positive_ratio 계산 (Service 책임)
        scored_df = self._calculate_positive_ratio(rest_df, review_df)

        print(rest_df['rest_y'].iloc[1])
        #print(rest_df['rest_y'].iloc[2])
        #print(rest_df['rest_y'].iloc[3])
        
        # 3. 추천 엔진 실행
        # 리뷰 추천도, 리뷰갯수, 거리로 최종 추천 점수를 추가한 df반환
        try :
            scored_df = self.engine.rest_score(
                user_lat        = user_lat,
                user_lon        = user_lon,
                rest_df         = scored_df,
                max_distance_km = max_distance_km
            )
            if scored_df.empty :
                return scored_df
        except Exception as e :
            print(e)
            raise ValueError(f"조회한 db에서 필수 컬럼이 없습니다. : {e}")
        # 필수 컬럼 누락 예외
        # 빈 df처리
        # 점수계산 안된 df
        
        #print("+_" * 25)
        # 4. 점수 기준 정렬 후 TOP-N
        result = (
            scored_df
            .sort_values('final_score', ascending=False)
            .head(top_n)
            .reset_index(drop=True)
        )
        
        #print("+_" * 25)
        return result