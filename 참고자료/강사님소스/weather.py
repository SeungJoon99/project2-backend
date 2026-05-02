import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# 1. 데이터 준비 
df = pd.read_csv("weather.csv",encoding="euc-kr")

print("--- 학습 데이터 미리보기 ---")
print(df.head())
print("-" * 30)

# 2. 데이터 전처리 (문자열 데이터를 숫자로 변환)
# 각 컬럼별로 LabelEncoder를 생성하여 저장해둡니다 (나중에 예측할 때 다시 사용)
le_dict = {}
cols_to_encode = ['온도', '습도', '강우량', '음식명']

for col in cols_to_encode:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

# 3. 독립변수(X)와 종속변수(y) 분리
X = df[['온도', '습도', '강우량']]
y = df['음식명']

# 4. 머신러닝 모델 학습 (Random Forest Classifier)
# 데이터가 적으므로 별도의 검증셋 분리 없이 전체 데이터로 학습합니다.
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# 5. 추천 함수 정의
def recommend_food(temp, humidity, rain, top_n=3):
    try:
        # 입력된 조건 인코딩 (학습 때 사용한 라벨과 동일하게 변환)
        input_data = pd.DataFrame({
            '온도': [le_dict['온도'].transform([temp])[0]],
            '습도': [le_dict['습도'].transform([humidity])[0]],
            '강우량': [le_dict['강우량'].transform([rain])[0]]
        })
        
        # 각 음식(클래스)별 확률 예측
        probs = rf_model.predict_proba(input_data)[0]
        
        # 확률이 높은 순서대로 인덱스 정렬
        top_indices = np.argsort(probs)[::-1][:top_n]
        
        print(f"\n[조건] 온도: {temp}, 습도: {humidity}, 강우량: {rain}")
        print(f"추천 음식 Top {top_n}:")
        
        # 인덱스를 다시 음식 이름으로 변환하여 출력
        for i, idx in enumerate(top_indices):
            food_name = le_dict['음식명'].inverse_transform([idx])[0]
            probability = probs[idx] * 100
            print(f"{i+1}위: {food_name} (추천 적합도: {probability:.1f}%)")
            
    except ValueError as e:
        print("오류: 학습 데이터에 존재하지 않는 조건 값이 입력되었습니다.")
        print(e)

# 6. 실제 예측 실행
# 요청하신 조건: 온도=추움, 습도=보통, 강우량=하
recommend_food(temp='추움', humidity='보통', rain='하', top_n=3)


