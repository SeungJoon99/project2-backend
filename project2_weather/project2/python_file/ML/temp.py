# import re
# import pandas as pd
# #특문, 결측값, 날짜변환 등

# # 데이터 로드
# # 사전에 날짜컬럼 변환처리 필요
# #df = pd.read_csv('../../data/01.원본데이터/리뷰/review_list2.csv', encoding='cp949')
# df = pd.read_csv('../../data/04.전처리_리뷰/list_clean3_utf8_emotion.csv')

# print(df.info())

# temp = df['clean_review'].astype(str).str.strip() == ''
# print(temp.sum()) #공백리뷰 개수
# temp = df[df['clean_review'].astype(str).str.strip() == '']
# print(temp) #공백리뷰 출력
# df = df.dropna(subset=['clean_review'])
# df = df[df['clean_review'].astype(str).str.strip() != '']

# print("++" * 25)
# print(df.info())

# df.to_csv('list_clean3_utf8_emotion.csv', index=False, encoding='utf-8-sig')
import pandas as pd

col = ['col1','col2','col3']
data = [[1,2,3], [4,5,6], [7,8,9]]
df = pd.DataFrame(data, columns=col)
print(df)
print(df.apply(sum))