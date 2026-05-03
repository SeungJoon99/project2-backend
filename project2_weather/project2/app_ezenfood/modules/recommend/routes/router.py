from flask import Blueprint, request, jsonify
from app_ezenfood.modules.recommend.service.reco_service import RestaurantRecommendService
from app_ezenfood.modules.recommend.service.review_service import ReviewService
from app_ezenfood.modules.recommend.service.category_service import CategoryRecommendService
from app_ezenfood.modules.recommend.DAO.review_dao import ReviewDAO
from app_ezenfood.modules.map_api.map_service import MapService
from app_ezenfood.modules.utils.get_conn import get_root_conn
from dotenv import load_dotenv
import pandas as pd
import os

recommend_bp = Blueprint(
    "recommend",
    __name__,
    url_prefix="/api/recommend"
)
recommend_service = RestaurantRecommendService()
category_service  = CategoryRecommendService()
map_service       = MapService()
load_dotenv()
WEATHER_KEY = os.getenv("WEATHER_API_KEY")

# 카테고리 추천 API
@recommend_bp.route("/categories", methods=["GET"])
#@recommend_bp.route("/<weather>", methods=["GET"])
def recommend_categories() :
    """
    필수 파라미터 :
    - lat               유저 위도 (y)
    - lon               유저 경도 (x)
    선택 :
    - top_n             추천할 카테고리 개수 limit
    """
    
    try :
        user_lat = float(request.args.get("lat"))
        user_lon = float(request.args.get("lon"))
    except (TypeError, ValueError) :
        return jsonify({
            "error" : "lat, lon은 필수이며 숫자여야 합니다."
        }), 400
    top_n        = int(request.args.get("top_n", 5))
    
    # 날씨 조회
    weather = map_service.get_weather(user_lat, user_lon, WEATHER_KEY)
    
    # 카테고리 추천
    try :
        result = category_service.recommend(weather)
    except Exception as e :
        return jsonify({"error" : "카테고리 추천 실패"}), 500
    return jsonify(result)


# 음식점 추천 API
@recommend_bp.route("/restaurants", methods=["GET"])
#@recommend_bp.route("/<category>", methods=["GET"])
def recommend_restaurants() :
    """
    필수 파라미터 :
    - sub_id            카테고리 아이디
    - lat               유저 위도 (y)
    - lon               유저 경도 (x)
    선택 :
    - max_distance_km   최대거리
    - top_n             음식점 몇 개 까지 가져올건지 limit
    """

    try :
        sub_id   = int(request.args.get("sub_id"))
        user_lat = float(request.args.get("lat"))
        user_lon = float(request.args.get("lon"))
    except (TypeError, ValueError) :
        return jsonify({
            "error": "sub_id, lat, lon은 필수이며 숫자여야 합니다."
        }), 400

    max_distance_km = float(request.args.get("distance", 1.5))
    top_n           = int(request.args.get("top_n", 5))

    try :
        result_df = recommend_service.recommend_restaurants(
            sub_id          = sub_id,
            user_lat        = user_lat,
            user_lon        = user_lon,
            max_distance_km = max_distance_km,
            top_n           = top_n
        )
    except (ValueError) :
        return jsonify({
            "error": "반경 내에 음식점이 없습니다."
        }), 400
        
    if result_df.empty :
        return jsonify({"restaurants" : []})
    return jsonify({
        "count"       : len(result_df),
        "restaurants" : result_df.to_dict(orient="records")
    }), 200

    """ 응답 예제 :
    {
        "count": 5,
        "restaurants": [
        {
            "distance_km": 0.257616157970359,
            "distance_score": 0.795155178042463,
            "final_score": 0.584031035608493,
            "positive_ratio": 0.25,
            "positive_reviews": 0,
            "rest_addr": "전북특별자치도 전주시 완산구 풍남문3길 26",
            "rest_id": 3322,
            "rest_name": "양식당",
            "rest_old": "전북특별자치도 전주시 완산구 전동 110-1",
            "rest_x": 127.1471442,
            "rest_y": 35.814932,
            "review_count": 140,
            "review_score": 1,
            "sentiment_score": 0.25,
            "total_reviews": 10
        }, * top_n
    """

# 리뷰 insert API
@recommend_bp.route("/reviews/import", methods=["POST"])
def import_reviews() :

    review_service = ReviewService()
    review_dao     = ReviewDAO(get_root_conn)

    df         = pd.read_csv("app_ezenfood/csv/reviews_repredicted.csv")
    mapped_df  = review_service.attach_rest_id(df)

    success_df = mapped_df[mapped_df['rest_id'].notna()]
    review_dao.insert_reviews(success_df)

    return jsonify({
        "inserted" : len(success_df),
        "failed"   : len(mapped_df) - len(success_df)
    })