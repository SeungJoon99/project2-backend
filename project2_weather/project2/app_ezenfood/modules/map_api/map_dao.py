import mysql.connector
import os

class MapDAO:
    def __init__(self):
        db_host = os.environ.get('DB_HOST', '127.0.0.1')
        db_port = int(os.environ.get('DB_PORT', 3306))
        db_user = os.environ.get('DB_USER', 'root')
        db_password = os.environ.get('DB_PASSWORD', 'ezen')
        db_name = os.environ.get('DB_NAME', 'defaultdb')

        try:
            self.conn = mysql.connector.connect(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_password,
                database=db_name,
                charset="utf8mb4"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except Exception as e:
            print(f"[ERROR] DB Connection Failed: {e}")
            raise e

    def fetch_restaurants(self, lat, lon, food_sort=None, limit=30):
        sql = """
        SELECT rest_name, rest_x, rest_y, rest_dong, rest_addr, review_count, rest_old
        FROM rest
        WHERE 1=1
        """
        params = []

        if food_sort:
            # DESC 결과에 따라 컬럼명을 sub_id로 수정
            sql += " AND sub_id = %s"
            params.append(food_sort)

        sql += " ORDER BY ABS(rest_y - %s) + ABS(rest_x - %s) LIMIT %s"
        params.extend([lat, lon, limit])

        try:
            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            for r in result:
                r["distance"] = self._calculate_distance(lat, lon, r["rest_y"], r["rest_x"])
            return result
        except Exception as e:
            print("[ERROR] DB 조회 실패:", e)
            return []

    def search_restaurants_by_name(self, query, lat, lon, limit=30):
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
            for r in results:
                r["distance"] = self._calculate_distance(lat, lon, r["rest_y"], r["rest_x"])
            return results
        except Exception as e:
            print(f"[ERROR] search_restaurants_by_name 실패:", e)
            return []

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        from math import sin, cos, sqrt, atan2, radians
        try:
            R = 6371
            dLat = radians(float(lat2) - float(lat1))
            dLon = radians(float(lon2) - float(lon1))
            a = sin(dLat/2)**2 + cos(radians(float(lat1))) * cos(radians(float(lat2))) * sin(dLon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            return R * c * 1000
        except:
            return 0