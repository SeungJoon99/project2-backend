import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
#from sklearn.metrics import accuracy_score, f1_score, classification_report
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 데이터 로드
tqdm.pandas()
df = pd.read_csv("csv/reviews_tokenized.csv")
df_emotionset = df
print(df.info())

# 결측행 제거
df_emotionset = df_emotionset.dropna(subset=['tokens'])
df_emotionset = df_emotionset.dropna(subset=['emotion'])
print(df_emotionset.info())

# 텍스트와 라벨
X = df_emotionset['tokens'].astype(str)
y = df_emotionset['emotion']   # 0 / 1 라벨


# 2. 훈련 / 테스트셋 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# 3. TF-IDF 벡터화
tfidf = TfidfVectorizer(
    max_features=20000,      # 단어 최대 수 (5만 리뷰 기준 적절)
    ngram_range=(1, 2),      # bigram 포함하면 성능 상승
    min_df=3                 # 3회 미만 등장 단어 제거
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)


# 4. 모델 학습
lr = LogisticRegression(
    max_iter=300,
    C=1.0,
    class_weight='balanced',   # 데이터 불균형 대비
    n_jobs=-1
)
lr.fit(X_train_tfidf, y_train)


# 5. 예측&평가
y_pred = lr.predict(X_test_tfidf)

print("Accuracy :", metrics.accuracy_score(y_test, y_pred))
print("F1 Score :", metrics.f1_score(y_test, y_pred))
print("\nClassification Report:\n", metrics.classification_report(y_test, y_pred))
print("Confusion matrix:\n{}".format(metrics.confusion_matrix(y_test, y_pred)))

# 모델의 계수(coefficients) 가져오기
coef = lr.coef_[0]
features = tfidf.get_feature_names_out()

# 데이터프레임 변환 후 상위/하위 단어 추출
df_coef = pd.DataFrame({'word': features, 'coefficient': coef})
top_positive = df_coef.sort_values(by='coefficient', ascending=False).head(10)
top_negative = df_coef.sort_values(by='coefficient', ascending=True).head(10)

# 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 시각화
plt.figure(figsize=(10, 6))
sns.barplot(data=pd.concat([top_positive, top_negative]), x='coefficient', y='word')
plt.title("Top Positive & Negative Words (LR Coefficients)")
plt.show()
"""
# 6. 새로운 리뷰 예측 함수
def predict_sentiment(text):
    vec = tfidf.transform([text])
    pred = lr.predict(vec)[0]
    prob = lr.predict_proba(vec)[0]
    print(text)
    if pred == 0:
        #print("부정리뷰")
        print(prob)
        return 0.0
    else:
        return print(f"긍정리뷰 {prob}")
    return pred, prob

print(predict_sentiment("음식이 정말 맛있고 친절했어요"))
print(predict_sentiment("짜고 서비스가 별로였습니다"))
print(predict_sentiment("맛없다 친절 하다"))
print(predict_sentiment("한참 먹다 삼계탕 바퀴벌레 나오다 먹다 식겁하다 황당하다 어렵다 자리 들다 크게 항의 못 먹다 사람 숟가락 놓다 밥값 받다"))
print(predict_sentiment("무한리필 계속 먹다 수 두번째 판 비주 얼다 달라지다 연어 껍질 부분 붙다 살 주다 더 비리 연어 살이 적다 느낌 원래 비주 얼 계속 괜찮다 금은 두번째 판 아쉽다 중간 열라면 먹다 딱이다 물이 한강 아쉽다"))
print(predict_sentiment("사진 두번째 리필 진키 오스 크다 리필 주문 하다 리필 해도 마음 불편하다 않다 주문 하다 퀄리티 좋다 연어 살 부위 경우 다르다 이해 하다 먹다 괜찮다 부위 나오다 좋다 차 끄다 오다 맥주 말다"))

idx = 578
#df['emotion'].iloc[idx] = predict_sentiment(df['tokens'].iloc[idx])
df.loc[idx, 'emotion'] = predict_sentiment(df.loc[idx, 'tokens'])
print(df['emotion'].iloc[idx])
print(df['emotion'].iloc[idx+1])
#test = predict_sentiment(df['tokens'].iloc[idx])
#print(test)

df['emotion'] = df['tokens'].progress_apply(predict_sentiment)
"""
# 긍정 편향된 모델이라 부정이라고 예측한 경우 부정 확률이 높을 것
# 예측 후 부정 확률이 높은 데이터만 선별하여 재학습에 활용

# 6. 리뷰 예측 함수 (확률 반환)
def pred_sentiment(text):
    vec = tfidf.transform([text])
    pred = lr.predict(vec)[0]  # 0 또는 1
    prob = lr.predict_proba(vec)[0] # [부정 확률, 긍정 확률]
    
    # 0.0과 prob(확률배열)을 튜플로 반환
    if pred == 0:
        return 0.0, prob[0] # (라벨, 부정 확률)
    else:
        return 1.0, prob[1] # (라벨, 긍정 확률)


# 예측
# 예측값과 확률을 각각의 컬럼에 저장
# df = df.dropna(subset=['tokens'])
# df['pred_emotion'], df['emotion_prob'] = zip(
#     *df['tokens'].progress_apply(pred_sentiment)
#     )
#df[['pred_emotion', 'emotion_prob']] = df['tokens'].progress_apply(
    # lambda x: pd.Series(pred_sentiment(x)))

# 결과 저장
#df.to_csv('reviews_predicted.csv', index=False, encoding='utf-8-sig')
