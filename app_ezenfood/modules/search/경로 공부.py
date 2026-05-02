import pandas as pd
import os

"""
    __file__ - 현재 실행 중인 파이썬 파일 경로 ) 여기서는 Github 어쩌구 나옴

    .abspath(__file__) - 절대 경로로 변환
        - 여기서는 이미 절대 경로지만, 절대 경로로 안전하게 맞춰주는 역할

    .dirname(...) - 파일이 있는 폴더 경로 추출

    .join - os에 맞춰서 경로들을 연결해줌 ex) 지금 여기서는 Github/어쩌구/../csv/filter_list.csv
"""
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # test.py 있는 폴더
print("base :",BASE_DIR)

csv_path = os.path.join(BASE_DIR, '..', 'csv', 'filter_list.csv')  # 상대경로 수정
print("csv :", csv_path)

df = pd.read_csv(csv_path)
print(df.info())


print("현재 작업 디렉터리:", os.getcwd())