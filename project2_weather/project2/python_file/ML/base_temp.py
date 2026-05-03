import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report

# 1. 데이터 로드
df = pd.read_csv("csv/reviews_tokenized.csv")
#df_emotionset = df
print(df.info())
#print(df_emotionset.info())
print("==" * 25)

# 결측행 제거
df = df.dropna(subset=['tokens'])
df = df.dropna(subset=['emotion'])
print(df.info())

pattern = r'^[가-힣0-9]+$'
clean_review = ~df['tokens'].astype(str).str.match(pattern)
print(clean_review.sum())
print(df[clean_review])

print(df.info())
#df = df['tokens']
#df.to_csv('tokens_only.csv', index=False, encoding='utf-8-sig')