import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import mglearn
import matplotlib.pyplot as plt
import random

# ------------------------------
# 1. 데이터 읽기 및 전처리
# ------------------------------
weather = pd.read_csv("\\504-m\공유\[2회차] 지능형 웹서비스 개발\03.프로젝트\02.팀프로젝트(2차)\D팀 - 최연흠,이승준,유재욱\파일업로드\이승준\2022년날씨데이터.csv")
weather["시간"] = pd.to_datetime(weather["시간"]).dt.hour

# 학습용 feature: 시간, 기온, 강수량, 습도
X = weather[["시간", "기온", "강수량", "습도"]].fillna(0)

# 스케일링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ------------------------------
# 2. KMeans 학습 (군집 수 6개)
# ------------------------------
kmeans = KMeans(n_clusters=6, random_state=42)
kmeans.fit(X_scaled)
weather["cluster"] = kmeans.labels_

# 군집 중심점 확인
centers = scaler.inverse_transform(kmeans.cluster_centers_)
centers_df = pd.DataFrame(centers, columns=X.columns)
print("군집 중심점:")
print(centers_df)

# 실루엣 점수
score = silhouette_score(X_scaled, kmeans.labels_)
print("\n실루엣 점수:", score)

# ------------------------------
# 3. 군집별 추천 음식 매핑
# ------------------------------
food_mapping = {
    0: ["토스트","샌드위치","바나나","사과","오렌지","오트밀","계란말이","치즈토스트","베이글","팬케이크",
        "햄버거","감자튀김","핫도그","베이컨","소시지","햄샌드위치","채소볶음","닭가슴살구이","스팀채소","볶음밥"],
    1: ["된장찌개","김치찌개","순두부찌개","삼계탕","갈비탕","떡국","칼국수","부대찌개","전골","우동",
        "해물탕","미역국","수제비","닭볶음탕","오므라이스","볶음밥","라면","짜장면","짬뽕","감자탕"],
    2: ["죽","토스트","간단 샌드위치","계란말이","베이글","치즈토스트","오트밀","햄버거","볶음밥","닭가슴살구이",
        "감자튀김","소시지","베이컨","스팀채소","햄샌드위치","오므라이스","라면","수제비","김밥","우동"],
    3: ["냉면","비빔국수","샐러드","쌈밥","잡채밥","김밥","오이무침","콩국수","두부조림","닭가슴살샐러드",
        "볶음밥","야채볶음밥","치킨샐러드","채소볶음","해물볶음","삼계죽","잡채","닭볶음탕","채소스튜","오므라이스"],
    4: ["샌드위치","토스트","햄버거","볶음밥","김밥","오므라이스","치킨","계란말이","베이컨","소시지",
        "햄샌드위치","스팀채소","야채볶음","닭가슴살구이","라면","수제비","칼국수","우동","파스타","잡채"],
    5: ["된장찌개","김치찌개","순두부찌개","삼계탕","갈비탕","떡국","칼국수","부대찌개","전골","우동",
        "해물탕","미역국","수제비","닭볶음탕","오므라이스","볶음밥","라면","감자탕","김밥","잡채"]
}

weather["추천 음식"] = weather["cluster"].apply(lambda c: random.choice(food_mapping[c]))

# ------------------------------
# 4. 테스트 입력
# ------------------------------
# 예: 현재 시간 15시, 기온 24도, 강수량 0, 습도 50
test_input = pd.DataFrame([[15, 24, 0, 50]], columns=["시간","기온","강수량","습도"])
test_scaled = scaler.transform(test_input)
cluster = kmeans.predict(test_scaled)[0]
recommended_food = random.choice(food_mapping[cluster])

print("\n테스트 입력:", test_input.values[0])
print("예측 군집:", cluster)
print("추천 음식:", recommended_food)

# ------------------------------
# 5. KMeans 알고리즘 설명 이미지
# ------------------------------

print("총 데이터 수:", X.shape[0])
print("사용한 feature 수:", X.shape[1])


# =====================================
# PCA 기반 군집분석 시각화
# =====================================
from matplotlib import rc
from sklearn.decomposition import PCA

# 한글 폰트
rc("font", family="gulim")

# PCA 변환 (2개 성분)
pca = PCA(n_components=2)
weather_pca = pca.fit_transform(X_scaled)

print(weather_pca)
print("=" * 30)

# 클러스터별 색상
colors = ["#476A2A", "#7851B8", "#BD3430", "#4A2D4E", "#875525",
          "#A83683", "#4E655E", "#853541", "#3A3120", "#535D8E"]

plt.figure(figsize=(10, 10))
plt.xlim(weather_pca[:, 0].min(), weather_pca[:, 0].max())
plt.ylim(weather_pca[:, 1].min(), weather_pca[:, 1].max())

for i in range(len(weather_pca)):
    # 군집 번호를 텍스트로 표시
    cluster_id = weather["cluster"].iloc[i]
    plt.text(
        weather_pca[i, 0],
        weather_pca[i, 1],
        str(cluster_id),
        color=colors[cluster_id % len(colors)],
        fontdict={'weight': 'bold', 'size': 9}
    )

plt.xlabel("첫 번째 주성분")
plt.ylabel("두 번째 주성분")
plt.title("날씨 데이터 PCA 2D 군집 시각화")
plt.show()

