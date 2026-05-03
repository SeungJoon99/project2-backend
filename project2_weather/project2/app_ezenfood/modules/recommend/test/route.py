from flask import Blueprint, render_template, request, redirect, session
import dao

#user에 관련된 라우터 함수들 분리
#@app.route("/login") -> @app.route("/user/login")

# @user_bp 데코레이터가 붙은 라우터는 전부 앞에 /user가 붙는다.
recommend_bp = Blueprint("recommend", __name__, url_prefix="/recommend")


#음식 카테고리 추천
#validate > service > dao
@recommend_bp.route("/recommend", methods=["GET"])
def recommend_category() :
    categorys = dao.get_food_category()
    return categorys

#음식점 추천
#validate > service > dao
@recommend_bp.route("/recommend/<category>", methods=["GET"])
def recommend_rest(category) :
    restaurants = ""
    if category == "all" :
        restaurants = dao.get_all_restaurants()
    else :
        restaurants = dao.get_recommend_restaurants(category)
    return restaurants

@recommend_bp.route("/recommend", methods=["GET"])
def recommend():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    weather = request.args.get("weather")

    result = service.recommend(lat, lon, weather)
    return jsonify(result)

from flask import Blueprint, request, jsonify
from app_ezenfood.modules.recommend.test.reco_service import RestaurantRecommendService

bp = Blueprint("recommend", __name__)
service = RestaurantRecommendService()

@bp.route("/recommend/rest")
def recommend_rest():

    user_lat = float(request.args['lat'])
    user_lon = float(request.args['lon'])

    # DAO에서 가져왔다고 가정
    rest_df = ...

    result = service.recommend(
        user_lat=user_lat,
        user_lon=user_lon,
        rest_df=rest_df
    )

    return jsonify(result.to_dict(orient="records"))
