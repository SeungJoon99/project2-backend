import datetime
import json
# 확장 :
# JSON to CSV, Sort JSON objects
# JSON Tools : Ctrl+Alt+M for JSON pretty, Alt+M for JSON minify
# > json파일에서만 동작;
data = {'response': {'header': {'resultCode': '10', 'resultMsg': '최근 1일 간의 자료만 제공합니다.'
        }
    }
}

print(data['response']['header']['resultCode'])

if data['response']['header']['resultCode'] :
    #정상 응답
    print()
else :
    #에러가 응답된 경우
    print("오류 :",
        data['response']['header']['resultCode'],
        data['response']['header']['resultMsg'])

data = {
    'response': {'header': {'resultCode': '00', 'resultMsg': 'NORMAL_SERVICE'}, 'body': {'dataType': 'JSON', 'items': {'item': [{'baseDate': '20251121', 'baseTime': '1000', 'category': 'PTY', 'nx': 55, 'ny': 127, 'obsrValue': '0'}, {'baseDate': '20251121', 'baseTime': '1000', 'category': 'REH', 'nx': 55, 'ny': 127, 'obsrValue': '32'}, {'baseDate': '20251121', 'baseTime': '1000', 'category': 'RN1', 'nx': 55, 'ny': 127, 'obsrValue': '0'}, {'baseDate': '20251121', 'baseTime': '1000', 'category': 'T1H', 'nx': 55, 'ny': 127, 'obsrValue': '9.5'}, {'baseDate': '20251121', 'baseTime': '1000', 'category': 'UUU', 'nx': 55, 'ny': 127, 'obsrValue': '1'}, {'baseDate': '20251121', 'baseTime': '1000', 'category': 'VEC', 'nx': 55, 'ny': 127, 'obsrValue': '214'}, {'baseDate': '20251121', 'baseTime': '1000', 'category': 'VVV', 'nx': 55, 'ny': 127, 'obsrValue': '1.5'}, {'baseDate': '20251121', 'baseTime': '1000', 'category': 'WSD', 'nx': 55, 'ny': 127, 'obsrValue': '1.8'}]}, 'pageNo': 1, 'numOfRows': 1000, 'totalCount': 8}}}


#요청 시 사용자 변수 입력 가능할 것(위치,시간)

#응답을 ml에 넣을 수 있게 변환할 것