from flask import Blueprint, request, jsonify
from .map_service import MapService
import os
from .map_dao import MapDAO

map_dao = MapDAO()

map_bp = Blueprint("map_bp", __name__)
service = MapService()

WEATHER_KEY = os.getenv("WEATHER_API_KEY")

# 기본 음식점 출력용 라우트
@map_bp.route("/restaurants", methods=["GET"])
def restaurants():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    food_sort = request.args.get("food_sort", default=None, type=str)
    limit = request.args.get("limit", default=30, type=int)

    if lat is None or lon is None:
        return jsonify({"error": "lat, lon 필요"}), 400

    data = service.get_restaurants(lat, lon, food_sort, limit)
    return jsonify(data)

# 좌표로 날씨 돌려주는 라우트
@map_bp.route("/weather", methods=["GET"])
def weather():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    print("WEATHER API HIT", lat, lon)
    if lat is None or lon is None:
        return jsonify({"error": "lat, lon 필요"}), 400
    data = service.get_weather(lat, lon, WEATHER_KEY)
    return jsonify(data)

# 음식점 검색 API
@map_bp.route("/search_restaurant/")
def search_restaurant():
    query = request.args.get("q", "").strip()
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if not query:
        return jsonify({"error": "검색어가 없습니다"}), 400
    if lat is None or lon is None:
        return jsonify({"error": "lat, lon 필요"}), 400

    restaurants = map_dao.search_restaurants_by_name(query, lat, lon)
    return jsonify({"restaurants": restaurants})
