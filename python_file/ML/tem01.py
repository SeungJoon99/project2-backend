import re
import pandas as pd
#특문, 결측값, 날짜변환 등

# 데이터 로드
# 사전에 날짜컬럼 변환처리 필요
df = pd.read_csv('../../data/01.원본데이터/리뷰/날짜변환/review_wdate_list4.csv', encoding='cp949')
#df = pd.read_csv('../../data/01.원본데이터/리뷰/review_list3.csv')
print(df.info())
print(df.head())
print("--" * 25)

# 정규화 함수
def normalize(text):
    # 한글, 숫자, 공백만 남기고 나머지 제거
    text = re.sub(r'[^ㄱ-ㅎ가-힣0-9\s]', '', text)

    # 반복 문자 축소 (예: ㅋㅋㅋㅋ → ㅋㅋ)
    text = re.sub(r'([ㄱ-ㅎ])\1{2,}', r'\1\1', text)

    # 공백 정리
    text = re.sub(r'\s+', ' ', text).strip()

    return text

pattern = r'^[가-힣0-9]+$'
#.apply(lambda x: bool(re.search(r'[^가-힣0-9]', x)))

# 상호 특문 처리
# 상호에 특문이 포함된 경우 TRUE
df['clean_rest'] = ~df['rest'].astype(str).str.match(pattern)
print(df['clean_rest'].sum())
print("--" * 25)
print(df[df['clean_rest']].head(100))
df = df.drop(columns="clean_rest")

# 리뷰 특문 검사
clean_review = ~df['review'].astype(str).str.match(pattern)

#print(df['clean_review'].sum())
#print(df[df['clean_review']])
print(clean_review.sum())


# 상호에 특문이 포함된 경우 행 제거
df = df[df['rest'].astype(str).str.match(pattern)]
# 상호 문자열타입으로 변환
df['rest'] = df['rest'].astype(str)

# 리뷰 전처리
df['clean_review'] = df['review'].apply(normalize).astype(str)
# 공백행 제거
temp = df['clean_review'].astype(str).str.strip() == ''
print(temp.sum()) # 공백리뷰 개수
temp = df[df['clean_review'].astype(str).str.strip() == '']
print(temp) # 공백리뷰 출력
df = df.dropna(subset=['clean_review']) # 결측행 제거
df = df[df['clean_review'].astype(str).str.strip() != ''] # 공백행 제거
print("++" * 25)

#날짜 변환
df['wdate'] = pd.to_datetime(df['wdate'], errors='coerce')

print(df.info())


#df['clean_review']

#df.to_csv('../../data/04.전처리_리뷰/list_clean4.csv', index=False)
df.to_csv('../../data/04.전처리_리뷰/list_clean4_utf8.csv', encoding='utf-8-sig', index=False)