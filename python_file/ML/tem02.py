import pandas as pd
from konlpy.tag import Okt
from tqdm import tqdm # 진행률 표시 라이브러리
# https://lovedh.tistory.com/entry/pandas-dataframe%EC%97%90%EC%84%9C-apply%EC%9D%98-%EC%A7%84%EC%B2%99%EB%8F%84-%EB%B3%B4%EA%B8%B0-tqdm

# 불용어, 토큰화, 벡터화 등

tqdm.pandas() # tqdm의 pandas전용 메소드를 호출
df = pd.read_csv('reviews.csv')
df.info()

okt = Okt()
index = 2
print(df.index)
text = df['clean_review'].iloc[index]
print(text)

# 추출할 품사 정의
target_pos = ['Noun', 'Adjective', 'Verb']

#all = okt.morphs(text, stem=True)
#pos = okt.pos(text, stem=True)
#nouns = okt.nouns(text)
#print(pos)
#print(pos[0][1])


# 불용어 집합
# set(집합)을 사용하면 조회성능이 향상
stopwords = set()
with open('stopwords-ko.txt', 'r', encoding='utf-8') as f:   #r : 읽기모드
    for line in f:
        #stopwords.append(line.strip())
        stopwords.add(line.strip())
print(stopwords)
#print(f"불용어 개수: {len(stopwords)}개")
#print(f"일부 불용어: {'나' in stopwords, '너' in stopwords, '우리' in stopwords, '가' in stopwords}")

#startswith()
# 기능: 문자열이 괄호 안의 특정 문자열로 시작하는지 검사
# 반환: 시작하면 True, 시작하지 않으면 False를 반환

""" 응애용 코드
#filtered_word = [word for word in words if word not in stopwords]
extracted_tokens = []
for i, text in enumerate(df['clean_review']):
    pos_result = okt.pos(text, stem=True)
    
    print(f"토큰화 진행률 : {(i + 1) / len(df) * 100}%", end='\r' )
    # 품사 필터링, 불용어 제거
    tokens = [
        word
        for word, tag in pos_result
        if tag in target_pos
        and word not in stopwords # 불용어 제거
    ]
    
    # 토큰들을 공백으로 연결하여 하나의 문자열로 변환
    filtered_word = ' '.join(tokens)  # 처리된 리뷰 문자열
    extracted_tokens.append(filtered_word) # 리스트에 추가
df['tokens'] = extracted_tokens
"""

# 진행률 표시 적용 토큰화 함수
# https://data-newbie.tistory.com/135
# loop(for문) 대신 apply와 tqdm.progress_apply 사용
# loop 사용시 효율 낮음
# pandas 연산은 벡터화 연산 + Cython(c언어기반?)이라 최적화시키면 성능 향상
def tokenizer(text) :
    pos_result = okt.pos(text, stem=True)
    
    # 품사 필터링, 불용어 제거
    tokens = [
        word for word, tag in pos_result
        if tag in target_pos
        and word not in stopwords # 불용어 제거
    ]
    #print(tokens)
    return ' '.join(tokens)

# tqdm 적용 토큰화
df['tokens'] = df['clean_review'].progress_apply(tokenizer)

#df.to_csv('reviews_tokenized.csv', index=False, encoding='utf-8-sig')