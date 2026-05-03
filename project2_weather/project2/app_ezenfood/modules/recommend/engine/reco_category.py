import os, pickle
import pandas as pd
import numpy as np
from app_ezenfood import PKL_DIR

# 🔹 모듈 로딩 시 한 번만 읽기
with open(os.path.join(PKL_DIR, 'kmeans_model.pkl'), 'rb') as f:
    KMEANS_MODEL = pickle.load(f)

with open(os.path.join(PKL_DIR, 'scaler_model.pkl'), 'rb') as f:
    SCALER_MODEL = pickle.load(f)

with open(os.path.join(PKL_DIR, 'cluster_name_map.pkl'), 'rb') as f:
    CLUSTER_NAME_MAP = pickle.load(f)

class CategoryRecommendEngine:
    def __init__(self) -> None:
        self.KMEANS_MODEL = KMEANS_MODEL
        self.SCALER_MODEL = SCALER_MODEL
        self.CLUSTER_NAME_MAP = CLUSTER_NAME_MAP

        if self.KMEANS_MODEL is None:
            raise RuntimeError("카테고리 추천 모델 로드 실패")

        
    # def _load_models(self) :
    #     try :
    #         with open(os.path.join(PKL_DIR, 'kmeans_model.pkl'), 'rb') as f :
    #             kmeans = pickle.load(f)
    #         with open(os.path.join(PKL_DIR, 'scaler_model.pkl'), 'rb') as f :
    #             scaler = pickle.load(f)
    #         with open(os.path.join(PKL_DIR, 'cluster_name_map.pkl'), 'rb') as f :
    #             cluster_map = pickle.load(f)
    #         print("모델 로드 완료 ✅")
    #         return kmeans, scaler, cluster_map
    #     except Exception as e :
    #         print("모델 로드 오류:", e)
    #         return None, None, None


    def recommend_food(self, features: dict) -> dict:
        features = features.copy()

        # pty 처리: 강수량 결정
        pty = features.get('pty', 0)
        rain = features.get('강수량', 0)
        features['강수량'] = 1.0 if pty in [1,2,3,4,5,6,7] else rain

        # SCALER 학습 시 사용한 컬럼만 남기고, 누락 컬럼은 0으로 채우기
        allowed_cols = self.SCALER_MODEL.feature_names_in_
        print(allowed_cols)
        df = pd.DataFrame([{col: features.get(col, 0) for col in allowed_cols}])

        # SCALER 변환
        X_scaled = self.SCALER_MODEL.transform(df)

        # KMeans 중심점 거리 계산
        distances = np.linalg.norm(self.KMEANS_MODEL.cluster_centers_ - X_scaled, axis=1)
        top3_ids = np.argsort(distances)[:3]
        top3_foods = [self.CLUSTER_NAME_MAP.get(int(i), "추천 정보 없음") for i in top3_ids]

        return {
            "top3_clusters": [int(i) for i in top3_ids],
            "recommendations": top3_foods
        }

    
    
    
    
    
    
    # def recommend_food(self, features : dict) -> dict :
    #     features = features.copy()

    #     # pty = features.get('pty', 0)
    #     # rain = features.get('강수량', 0)

    #     # # 삼항 연산자 참 if 조건 else 거짓
    #     # features['강수량'] = 1.0 if pty in [1,2,3,4,5,6,7] else rain
    #     # print("effective_rain : ", features['강수량'])

    #     # df = pd.DataFrame([features])
    #     # print("df : ", df)
    #     # X_scaled = self.SCALER_MODEL.transform(df)
    #     # print("X_scaled : ", X_scaled)

    #     # 학습 시 사용한 컬럼만 남기기
    #     allowed_cols = ["시간", "기온", "강수량", "습도"]
    #     df = pd.DataFrame([{k:v for k,v in features.items() if k in allowed_cols}])

    #     X_scaled = self.SCALER_MODEL.transform(df)

        
    #     # 중심점 거리 계산
    #     distances = np.linalg.norm(self.KMEANS_MODEL.cluster_centers_ - X_scaled, axis=1)
    #     print("distances : ", distances)
    #     print("--" * 25)
    #     top3_ids = np.argsort(distances)[:3]
    #     top3_foods = [self.CLUSTER_NAME_MAP.get(int(i), "추천 정보 없음") for i in top3_ids]

    #     return {
    #         "top3_clusters": [int(i) for i in top3_ids],
    #         "recommendations": top3_foods
    #     }
