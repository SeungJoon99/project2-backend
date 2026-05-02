from flask import jsonify
from app_ezenfood.modules.recommend.engine.reco_category import CategoryRecommendEngine
from app_ezenfood.modules.map_api.map_service import MapService
from datetime import datetime
from dotenv import load_dotenv
import os

class HomeController :
    def __init__(self) :
        pass

    def get_recommendation(self, args):
        #try:
            print("--" * 25)
            input_data = {
                "계절": int(args.get('season', 1)),
                "시": datetime.now().hour,
                "기온": float(args.get('temp', 20.0)),
                "강수량": float(args.get('rain', 0.0)),
                "풍속": float(args.get('wind', 0.0)),
                "습도": float(args.get('humidity', 50.0)),
                #"pty": int(args.get('pty', 0))
            }
            print("input_data :", input_data)
            print("_-" * 25)
            result = engine.recommend_food(input_data)
            print("result :", result)
            return result
        #except Exception as e:
            return {"error": str(e)}, 500


load_dotenv()
WEATHER_KEY = os.getenv("WEATHER_API_KEY")
print("apikey :", WEATHER_KEY)
a = HomeController()
service = MapService()
engine = CategoryRecommendEngine()
lat = 35.8150
lon = 127.1500
print("_+" * 30)
data = service.get_weather(lat, lon, WEATHER_KEY)
print("_+" * 25)
print("data :", data)
print("_+" * 25)
category = a.get_recommendation(data)
print("_+" * 25)
print(category)

#response = jsonify({"error": "test"})

# 테스트용 하드코딩 함수
def category_test(args) -> dict | tuple :
    try:
        features = {
            "계절": int(args.get('season', 1)),
            "시": datetime.now().hour,
            "기온": float(args.get('temp', 20.0)),
            "강수량": float(args.get('rain', 0.0)),
            "풍속": float(args.get('wind', 0.0)),
            "습도": float(args.get('humidity', 50.0)),
            "pty": int(args.get('pty', 0))
        }
        return features
    except Exception as e :
        return {"error": str(e)}, 500


result = engine.recommend_food(category_test())
print(result)