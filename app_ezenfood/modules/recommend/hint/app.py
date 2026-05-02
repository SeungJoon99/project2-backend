from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os
import pickle
from datetime import datetime
import pandas as pd
import numpy as np

load_dotenv()

# 환경 변수
KAKAO_MAP_KEY = os.getenv("KAKAO_MAP_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# --------------------------
# 경로 설정
# --------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))              # backend/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                          # 프로젝트 루트
MODEL_DATA_DIR = os.path.join(BASE_DIR, 'data')                   # backend/data

# --------------------------
# Flask 초기화
# --------------------------
app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, 'frontend', 'templates'),
    static_folder=os.path.join(PROJECT_ROOT, 'frontend', 'static')
)
CORS(app)

# --------------------------
# MySQL 설정
# --------------------------
DB_CONFIG = {
    'user': 'root',
    'password': 'ezen',
    'host': '127.0.0.1',
    'database': 'whateatnow'
}

EARTH_RADIUS_KM = 6371


# --------------------------
# 모델 로드 함수
# --------------------------
def load_models():
    try:
        kmeans_path = os.path.join(MODEL_DATA_DIR, 'kmeans_model.pkl')
        scaler_path = os.path.join(MODEL_DATA_DIR, 'scaler_model.pkl')
        map_path = os.path.join(MODEL_DATA_DIR, 'cluster_name_map.pkl')

        # 존재 여부 체크
        if not os.path.exists(kmeans_path):
            raise FileNotFoundError(f"KMeans 파일 없음: {kmeans_path}")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler 파일 없음: {scaler_path}")
        if not os.path.exists(map_path):
            raise FileNotFoundError(f"Mapping 파일 없음: {map_path}")

        # 로드
        with open(kmeans_path, 'rb') as f:
            kmeans_model = pickle.load(f)

        with open(scaler_path, 'rb') as f:
            scaler_model = pickle.load(f)

        with open(map_path, 'rb') as f:
            cluster_name_map = pickle.load(f)

        print("✅ 모델 로드 완료!")
        return kmeans_model, scaler_model, cluster_name_map

    except Exception as e:
        print(f"❌ 모델 로드 오류: {e}")
        return None, None, None


# 로드 실행
KMEANS_MODEL, SCALER_MODEL, CLUSTER_NAME_MAP = load_models()


# --------------------------
# 메인 화면
# --------------------------
@app.route('/')
def index():
    return render_template(
        'map.html',
        kakao_key=KAKAO_MAP_KEY,
        weather_key=WEATHER_API_KEY
    )


# --------------------------
# /api/recommend — 날씨 기반 추천 API
# --------------------------
@app.route('/api/recommend', methods=['GET'])
def get_recommendation():

    if KMEANS_MODEL is None:
        return jsonify({"error": "KMeans 모델 없음"}), 503

    try:
        pty = request.args.get('pty', 0, type=int)
        rain = request.args.get('rain', 0.0, type=float)
        wind = request.args.get('wind', 0.0, type=float)

        # 강수량 처리
        effective_rain = 1.0 if pty in [1, 2, 3, 4, 5, 6, 7] else rain

        input_data = {
            "계절": request.args.get('season', 1, type=int),
            "시": datetime.now().hour,
            "기온": request.args.get('temp', 20.0, type=float),
            "강수량": effective_rain,
            "풍속": wind,
            "습도": request.args.get('humidity', 50.0, type=float)
        }

        X_new = pd.DataFrame([input_data])
        X_scaled_new = SCALER_MODEL.transform(X_new)

        # 클러스터 거리 계산
        distances = np.linalg.norm(
            KMEANS_MODEL.cluster_centers_ - X_scaled_new, axis=1
        )

        top3_ids = np.argsort(distances)[:3]
        top3_foods = [CLUSTER_NAME_MAP.get(i, "추천 정보 없음") for i in top3_ids]

        return jsonify({
            "top3_clusters": [int(i) for i in top3_ids],
            "recommendations": top3_foods
        })

    except Exception as e:
        print("추천 API 오류:", e)
        return jsonify({"error": str(e)}), 500


# --------------------------
# /api/restaurants — 음식점 조회
# --------------------------
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    food_sort = request.args.get('food_sort', type=str)

    if lat is None or lon is None:
        return jsonify({"error": "위경도 필요"}), 400

    where_clause = "WHERE 1=1"
    where_params = []

    if food_sort:
        where_clause += " AND sort LIKE %s"
        where_params.append(f"%{food_sort}%")

    having_clause = "HAVING distance_km <= 1"

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        haversine_formula = f"""
        ({EARTH_RADIUS_KM} * acos(
            cos(radians(%s)) * cos(radians(y))
            * cos(radians(x) - radians(%s))
            + sin(radians(%s)) * sin(radians(y))
        ))
        """

        query = f"""
            SELECT r_name, y, x, dong, sort, addr, ads,
                {haversine_formula} AS distance_km
            FROM map
            {where_clause}
            {having_clause}
            ORDER BY distance_km ASC
            LIMIT %s OFFSET %s
        """

        query_params = [lat, lon, lat] + where_params + [limit, offset]

        cursor.execute(query, query_params)
        rows = cursor.fetchall()

        restaurants = [
            {
                "r_name": row["r_name"],
                "y": row["y"],
                "x": row["x"],
                "dong": row["dong"],
                "sort": row["sort"],
                "addr": row["addr"],
                "ads": row["ads"],
                "distance": int(row["distance_km"] * 1000)
            }
            for row in rows
        ]

        return jsonify(restaurants)

    except Exception as e:
        print("DB ERROR:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


# --------------------------
# 서버 시작
# --------------------------
if __name__ == '__main__':
    print("===================================================")
    print("🚀 Flask 서버 실행 중… http://127.0.0.1:5000/")
    print("===================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
