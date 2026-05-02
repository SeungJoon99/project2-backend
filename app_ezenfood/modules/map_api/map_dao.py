# map/map_dao.py
import mysql.connector

class MapDAO:
    """
    음식점 데이터 접근 계층 (Data Access Object, DAO)
    MySQL DB 연결 버전
    """
    def __init__(self):
        # MySQL DB 연결
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="ezen",
            database="whateatnow",
            charset="utf8mb4"
        )
        # 커서 생성 (dictionary=True → 컬럼명을 key로 사용)
        self.cursor = self.conn.cursor(dictionary=True)

    def fetch_restaurants(self, lat, lon, food_sort=None, limit=30):
        """
        lat/lon 기준 근처 음식점 데이터 반환
        food_sort가 None이면 전체 음식점 조회

        Parameters
        ----------
        lat : float
            기준 위도
        lon : float
            기준 경도
        food_sort : str, optional
            음식 종류 (예: "한식", "중식"), 기본값 None
        limit : int, optional
            조회할 최대 음식점 개수, 기본값 30

        Returns
        -------
        list[dict]
            조회된 음식점 리스트, 실패 시 빈 리스트 반환
        """
        # 변경된 컬럼명 기준 SELECT
        sql = """
        SELECT rest_name, rest_x, rest_y, rest_dong, rest_addr, review_count, rest_old, distance
        FROM restaurants
        WHERE 1=1
        """
        params = []

        # food_sort가 지정되어 있으면 WHERE 조건 추가
        if food_sort:
            sql += " AND sort = %s"
            params.append(food_sort)

        # 단순 거리 계산: 위도(y) 차이 + 경도(x) 차이 기준 정렬
        sql += " ORDER BY ABS(rest_y - %s) + ABS(rest_x - %s) LIMIT %s"
        params.extend([lat, lon, limit])

        try:
            # 쿼리 실행
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            # 조회된 개수 로그 출력 (디버깅 용도)
            print("[DEBUG] fetch_restaurants result count:", len(result))
            return result
        except Exception as e:
            # DB 조회 실패 시 에러 로그 출력
            print("[ERROR] DB 조회 실패:", e)
            return []  # 빈 리스트 반환


    def search_restaurants_by_name(self, query, lat, lon, limit=30):
        """
        이름 기반 음식점 검색 (부분일치) + 좌표 기준 거리 계산
        """
        sql = """
        SELECT rest_name, rest_x, rest_y, rest_dong, rest_addr, review_count, rest_old
        FROM rest
        WHERE rest_name LIKE %s COLLATE utf8mb4_general_ci
        ORDER BY ABS(rest_y - %s) + ABS(rest_x - %s)
        LIMIT %s
        """
        params = [f"%{query}%", lat, lon, limit]

        try:
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()

            # 거리 계산 (미터 단위)
            for r in results:
                r["distance"] = self._calculate_distance(lat, lon, r["rest_y"], r["rest_x"])

            print(f"[DEBUG] search_restaurants_by_name '{query}' result count:", len(results))
            return results
        except Exception as e:
            print(f"[ERROR] search_restaurants_by_name '{query}' 실패:", e)
            return []


    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        from math import sin, cos, sqrt, atan2, radians
        R = 6371  # 지구 반지름 km
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        a = sin(dLat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c * 1000  # m
