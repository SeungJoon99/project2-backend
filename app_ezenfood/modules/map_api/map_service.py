from .map_dao import MapDAO
import requests
from datetime import datetime, timedelta
import math


class MapService:
    def __init__(self):
        self.dao = MapDAO()

    # ==========================
    # 음식점 조회
    # ==========================
    def get_restaurants(self, lat, lon, food_sort=None, limit=30):
        try:
            return self.dao.fetch_restaurants(lat, lon, food_sort, limit)
        except Exception as e:
            print(f"[MapService] DB 조회 실패: {e}")
            return []

    # ==========================
    # 위경도 → 기상청 격자 변환
    # ==========================
    def dfs_xy_conv(self, lat, lon):
        RE, GRID = 6371.00877, 5.0
        SLAT1, SLAT2 = 30.0, 60.0
        OLON, OLAT = 126.0, 38.0
        XO, YO = 43, 136
        DEGRAD = math.pi / 180.0

        re = RE / GRID
        slat1 = SLAT1 * DEGRAD
        slat2 = SLAT2 * DEGRAD
        olon = OLON * DEGRAD
        olat = OLAT * DEGRAD

        sn = math.log(math.cos(slat1) / math.cos(slat2)) / \
             math.log(math.tan(math.pi * 0.25 + slat2 * 0.5) /
                      math.tan(math.pi * 0.25 + slat1 * 0.5))
        sf = math.pow(math.tan(math.pi * 0.25 + slat1 * 0.5), sn) * math.cos(slat1) / sn
        ro = re * sf / math.pow(math.tan(math.pi * 0.25 + olat * 0.5), sn)
        ra = re * sf / math.pow(math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5), sn)

        theta = lon * DEGRAD - olon
        if theta > math.pi:
            theta -= 2.0 * math.pi
        if theta < -math.pi:
            theta += 2.0 * math.pi
        theta *= sn

        x = math.floor(ra * math.sin(theta) + XO + 0.5)
        y = math.floor(ro - ra * math.cos(theta) + YO + 0.5)

        return {"x": x, "y": y}

    # ==========================
    # 기상청 초단기예보
    # ==========================
    def get_weather(self, lat, lon, service_key):
        # 1️⃣ 좌표 변환
        coords = self.dfs_xy_conv(lat, lon)
        nx, ny = coords["x"], coords["y"]

        # 2️⃣ base_time 계산
        #     - 매시 30분 발표
        #     - 00~44분 → 이전 시각 사용
        now = datetime.now()
        if now.minute < 45:
            now -= timedelta(hours=1)

        base_date = now.strftime("%Y%m%d")
        base_time = now.strftime("%H") + "00"

        # 3️⃣ API 설정
        url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
        params = {
            "serviceKey": service_key,
            "numOfRows": 100,
            "pageNo": 1,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": nx,
            "ny": ny
        }

        CATEGORY_MAP = {
            "T1H": "temp",
            "RN1": "rain",
            "REH": "humidity",
            "SKY": "sky",
            "PTY": "pty",
            "WSD": "wind_speed",
            "UUU": "wind_u",
            "VVV": "wind_v",
            "VEC": "wind_dir",
            "LGT": "lightning",
            "SNO": "snow"
        }

        def to_float(v):
            try:
                return float(v)
            except:
                return None

        # 기본 반환 구조 (절대 프론트로 -- 안 보냄)
        def empty_weather():
            return {
                "temp": None,
                "rain": 0,
                "humidity": None,
                "sky": None,
                "pty": None,
                "wind_speed": None,
                "wind_u": None,
                "wind_v": None,
                "wind_dir": None,
                "snow": 0,
                "lightning": None
            }

        try:
            # 4️⃣ API 호출
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            items = (
                data.get("response", {})
                    .get("body", {})
                    .get("items", {})
                    .get("item", [])
            )

            if not items:
                return empty_weather()

            # 5️⃣ fcstDate + fcstTime 목록 정렬
            times = sorted(set(
                (i["fcstDate"], i["fcstTime"]) for i in items
            ))

            # 6️⃣ base_time 기준 가장 가까운 fcstTime 선택
            now_key = (base_date, base_time)
            target_time = None

            for t in times:
                if t >= now_key:
                    target_time = t
                    break

            if target_time is None:
                target_time = times[-1]

            # ==========================
            # 🔥 핵심 로직
            # fcstTime을 30분씩 뒤로 탐색
            # ==========================
            MAX_RETRY = 6  # 최대 3시간
            retry = 0

            while retry < MAX_RETRY:
                weather = empty_weather()

                target_items = [
                    i for i in items
                    if (i["fcstDate"], i["fcstTime"]) == target_time
                ]

                for it in target_items:
                    cat = it.get("category")
                    val = it.get("fcstValue")

                    if cat not in CATEGORY_MAP:
                        continue

                    key = CATEGORY_MAP[cat]

                    if key in ("sky", "pty"):
                        if str(val).isdigit():
                            weather[key] = int(val)
                    else:
                        v = to_float(val)
                        if v is not None:
                            weather[key] = v

                # ✅ temp / sky / pty 모두 있으면 즉시 반환
                if (
                    weather["temp"] is not None and
                    weather["sky"] is not None and
                    weather["pty"] is not None
                ):
                    return weather

                # ❌ 하나라도 없으면 30분 이전 시각으로 이동
                target_dt = datetime.strptime(
                    target_time[0] + target_time[1],
                    "%Y%m%d%H%M"
                ) - timedelta(minutes=30)

                target_time = (
                    target_dt.strftime("%Y%m%d"),
                    target_dt.strftime("%H%M")
                )

                retry += 1

            # 여기까지 왔다는 건 극히 예외
            return weather

        except Exception as e:
            print(f"[Weather API error] {e}")
            return empty_weather()
