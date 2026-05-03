import pandas as pd
from app_ezenfood.modules.utils.distance_module import haversine

# 사용자 위치, 리뷰 수, 리뷰 감성 점수 기반 음식점 추천 엔진
class RestaurantRecommendationEngine:

    # 생성자, 가중치 설정
    def __init__(
        self,
        sentiment_weight: float = 0.5,
        review_weight: float = 0.3,
        distance_weight: float = 0.2
    ):
        self.sentiment_weight = sentiment_weight
        self.review_weight = review_weight
        self.distance_weight = distance_weight

    # 거리 계산 메서드
    def _calculate_distance(
        self,
        df: pd.DataFrame,
        user_lat: float,
        user_lon: float
    ) -> pd.DataFrame:
        # 사용자와 음식점 간 거리 계산(km)
        # x1, y1 : 이용자 x, y 좌표
        # x2, y2 : 가게 x, y 좌표
        df['distance_km'] = df.apply(
            lambda row: haversine(
                user_lat, user_lon,
                row['rest_y'], row['rest_x']
            ),
            axis=1
        )
        return df

    # 추천 점수 산출 로직
    def rest_score(
        self,
        user_lat: float,
        user_lon: float,
        rest_df: pd.DataFrame,
        max_distance_km: float = 1.0
    ) -> pd.DataFrame:

        df = rest_df.copy()

        # 필수 컬럼 체크
        required_cols = {
            'rest_x', 'rest_y', 'review_count', 'positive_ratio'
        }
        missing = required_cols - set(df.columns)
        if missing:
            # 컬럼 누락시 오류생성
            raise ValueError(f"필수 컬럼 누락: {missing}")

        # 1. 거리 계산
        df = self._calculate_distance(df, user_lat, user_lon)
        # 반경을 벗어나는 음식점 컷오프
        df = df[df['distance_km'] <= max_distance_km]
        if df.empty:
            return df

        # 2. 점수 정규화
        # .clip : 범위를 초과 한 값은 잘라냄
        # 감성 점수
        df['distance_score']  = 1 / (1 + df['distance_km'])
        # 리뷰 수 점수
        df['review_score']    = (df['review_count'] / 100).clip(0, 1)
        # 거리 점수
        df['sentiment_score'] = df['positive_ratio'].clip(0, 1)

        # 3. 최종 점수 계산
        df['final_score'] = (
            df['sentiment_score'] * self.sentiment_weight +
            df['review_score']    * self.review_weight +
            df['distance_score']  * self.distance_weight
        )

        return df