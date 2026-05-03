from datetime import datetime

# 받은 날씨를 엔진에 입력가능한 형태로 변환하는 모듈
class WeatherToFeature :
    def __init__(self) -> None :
        pass
    
    # 계절 계산 함수
    def _get_season(self) -> int :
        m = datetime.now().month
        
        if   m <= 2 : return 4  # 겨울
        elif m <= 5 : return 1  # 봄
        elif m <= 8 : return 2  # 여름
        else        : return 3  # 가을

    # df용 dict로 변환
    def build(self, weather : dict) -> dict :
        return {
            "계절"   : self._get_season(),
            "시"     : datetime.now().hour,
            "기온"   : weather["temp"],
            "강수량" : weather["rain"],
            "풍속"   : weather.get("wind_speed", 0),
            "습도"   : weather.get("humidity", 50),
            "pty"    : weather.get("pty", 0) # 수정필요
            # pyt 아마 모델이 못 받는듯
        }
