import pandas as pd
from app_ezenfood.modules.utils.weather_to_feature import WeatherToFeature
from app_ezenfood.modules.recommend.DAO.reco_dao import RecommendDAO
from app_ezenfood.modules.recommend.engine.reco_category import CategoryRecommendEngine

class CategoryRecommendService :
    
    def __init__(self) :
        self.feature_builder = WeatherToFeature()
        self.engine = CategoryRecommendEngine()

    # 날씨 dict를 받아 음식 카테고리 추천 결과 반환
    def recommend(self, weather : dict) -> dict :
        features = self.feature_builder.build(weather)
        try :
            return self.engine.recommend_food(features)
        except Exception as e :
            print(e)
            return {"error" : str(e)}


    # 클러스터id와 카테고리id 매핑