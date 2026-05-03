import requests
import datetime
import json

now = datetime.datetime.now()
base_date = now.strftime("%Y%m%d")  # 오늘
base_time = now.strftime("%H00")    # 현재시간 정각

# url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey= &numOfRows=10&dataType=json&pageNo=1&base_date=20210628&base_time=0600&nx=55&ny=127'

#api 요청 데이터
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = {
    'serviceKey' : '',
    'pageNo' : '1',
    'numOfRows' : '1000',
    'dataType' : 'json',
    'base_date' : base_date,
    'base_time' : base_time,
    'nx' : '55',
    'ny' : '127'
}  #오류 요청 = 'base_date' : '20210628', 'base_time' : '0600'

#응답 변수
response = requests.get(url, params=params)
#print("바이트응답 : ")
#print(response.content)  #응답 출력
print("서버인코딩 : ")
print(response.text)     #서버가 보낸 인코딩대로 디코딩

#json 파싱
data = response.json()
print("json파싱 : ")
print(data)

"""
#.json 읽기
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(data)

#.json 저장
data = {"name": "홍길동", "age": 20}
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
"""
#.csv 저장