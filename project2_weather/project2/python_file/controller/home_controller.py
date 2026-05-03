from flask import jsonify, render_template
from app_ezenfood.modules import db_module
from datetime import datetime
import os
from dotenv import load_dotenv

from app_ezenfood.modules.recommend.engine.reco_category import CategoryRecommendEngine

load_dotenv()

KAKAO_MAP_KEY = os.getenv("KAKAO_MAP_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
engine = CategoryRecommendEngine()
class HomeController:
    def index(self):
        return render_template('map.html', kakao_key=KAKAO_MAP_KEY, weather_key=WEATHER_API_KEY)

    def get_recommendation(self, args):
        try:
            input_data = {
                "계절": int(args.get('season', 1)),
                "시": datetime.now().hour,
                "기온": float(args.get('temp', 20.0)),
                "강수량": float(args.get('rain', 0.0)),
                "풍속": float(args.get('wind', 0.0)),
                "습도": float(args.get('humidity', 50.0)),
                "pty": int(args.get('pty', 0))
            }
            result = engine.recommend_food(input_data)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_restaurants(self, args):
        try:
            lat = float(args.get('lat'))
            lon = float(args.get('lon'))
            # 
            offset = int(args.get('offset', 0))
            # 
            limit = int(args.get('limit', 10))
            # 단일 카테고리
            food_sort = args.get('food_sort')

            restaurants = db_module.get_nearby_restaurants(lat, lon, offset, limit, food_sort)
            return jsonify(restaurants)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
