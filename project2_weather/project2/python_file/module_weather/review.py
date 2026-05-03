data = [
    {
        'code' : '379218',
        'store_name' : '박가네',
        'review' : [
            {'2025-01-01' : '기본안주가 너무맛있어요!!'},
            {'2025-05-12' : '별로에요'},
            {'2025-09-20' : '친구들니랑 청첩장 모임했어요 너무 맛있게 먹었어요!!!'},
            {'2025-10-25' : '가성비 최고 시장집👍🏻 싼데 양도 많고 맛있어요ㅠ'},
            {'2025-07-21' : '음식도 맛있고 양이 푸짐해요! 기대보다 양이 너무 많아서 3만원 코스에 남자 3명이서 배부르게 먹고 나왔습니다 팥빙수 서비스도 나와서 후식까지 맛있게 먹었습니다. 재방문 의사 높습니다!!'}
        ]
    },
    {
        'code' : '32284835',
        'store_name' : '표주박',
        'review' : [
            {'2025-06-20' : '비가 너무 많이 와서 깜빡하고...'},
            {'2025-03-02' : '아이가 한옥에서 자보고싶다고해서 왔는데 생각이상으로 예쁘고 아이가 너무 좋아했어요'},
            {'2025-06-13' : '전주한옥마을에 오시는 10명 전후의 단체 여행팀이면 더욱 이용에 편리한  숙소로 추천~'},
            {'2025-07-21' : '조용히 쉬기 좋아요'},
            {'2025-06-06' : '가족과 좋은시간 잘 보내고 왔습니다'}
        ]
    },
    {
        'code' : '37944209',
        'store_name' : '누룩꽃피는날',
        'review' : [
            {'2025-07-03' : '사진은 못 찍었는데 짜빠구리도 맛있어요.'},
            {'2024-10-03' : '전주 여행와서 모주 먹어보려고 들른 곳 보쌈 양이 푸짐해서 좋았습니다~ 모주는 기대했는데 제 취향은 아니었던 걸로🤣'},
            {'2024-11-23' : '음식이 맛있어요'},
            {'2024-09-08' : '조아요'},
            {'2024-03-16' : '긋'}
        ]
    },
]

import pandas as pd

data = {}  # 제공된 'data' 변수가 여기에 있다고 가정

# 1. 데이터를 평탄화하여 리스트에 담는 과정
flat_data = []
for store in data:
    store_code = store['code']
    store_name = store['store_name']
    
    # 각 가게의 리뷰 리스트를 반복 처리
    for review_dict in store['review']:
        # 딕셔너리에서 key(날짜)와 value(내용)를 분리
        date = list(review_dict.keys())[0]
        content = list(review_dict.values())[0]
        
        # 새로운 레코드(행) 생성
        flat_data.append({
            'code': store_code,
            'store_name': store_name,
            'review_date': date,
            'review_content': content
        })

# 2. pandas df로 변환
df = pd.DataFrame(flat_data)

# 확인
# print(df.head())

"""
1. 시계열 분석 가능: review_date를 날짜/시간 타입으로 변환하여 시간 경과에 따른 리뷰 변화를 쉽게 분석가능

2. 텍스트 분석 용이: review_content만 추출하여 감성 분석(Sentiment Analysis)이나 토픽 모델링 등의 자연어 처리(NLP) 기법을 바로 적용가능

3. 데이터 분리: 가게 정보(code, store_name)는 범주형 피처로, 리뷰 내용(review_content)은 텍스트 피처로 명확하게 분리되어 모델 학습에 사용하기 용이

날짜 피처 확장:
주말에 작성된 리뷰인지 여부 등을 새로운 범주형 피처로 사용 (예: 월, 요일, 분기)

범주형 피처 인코딩:
code와 store_name을 Label Encoding이나 Embedding을 통해 모델이 이해할 수 있는 수치형 벡터로 변환
"""
data = [
    {
        'code': '379218',
        'store_name': '박가네',
        'review_date': '2025-01-01',
        'review_text': '기본안주가 너무맛있어요!!'
    },
    {
        'code': '379218',
        'store_name': '박가네',
        'review_date': '2025-05-12',
        'review_text': '별로에요'
    },
    {
        'code': '379218',
        'store_name': '박가네',
        'review_date': '2025-09-20',
        'review_text': '친구들니랑 청첩장 모임했어요 너무 맛있게 먹었어요!!!'
    },
    {
        'code': '32284835',
        'store_name': '표주박',
        'review_date': '2025-06-20',
        'review_text': '비가 너무 많이 와서 깜빡하고 숙소 사진을 못 찍었어요ㅎ...'
    },
    {
        'code': '37944209',
        'store_name': '누룩꽃피는날',
        'review_date': '2024-03-16',
        'review_text': '긋'
    }
]


"""
분석	    날짜별 리뷰 수, 감성 분석 등 가능
머신러닝	 review_text만 NLP 처리하면 됨
CSV	        1 리뷰 = 1 row 구조
DB	        store 테이블과 review 테이블로 정규화 가능
가독성	    사람이 봐도 구조가 직관적

긍/부정 라벨링
날짜 정렬 / 통계 처리
가게별 평균 감성 스코어 모델
"""