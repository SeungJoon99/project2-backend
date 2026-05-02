import psycopg2
import os
from .utils.distance_module import haversine

# DATABASE_URL 사용
DATABASE_URL = "postgresql://postgres:pUHTRvwAodiaHvlFWLPoDhJeqVSpblBb@switchyard.proxy.rlwy.net:28520/railway"

def get_nearby_restaurants(lat, lon, offset=0, limit=10, food_sort=None):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    where_clause = "WHERE 1=1"
    params = []

    if food_sort:
        where_clause += " AND sort LIKE %s"
        params.append(f"%{food_sort}%")

    haversine_formula = """
    (6371 * acos(
        cos(radians(%s)) * cos(radians(y))
        * cos(radians(x) - radians(%s))
        + sin(radians(%s)) * sin(radians(y))
    ))
    """

    query = f"""
        SELECT r_name, y, x, dong, sort, addr, ads,
               {haversine_formula} AS distance_km
        FROM map
        {where_clause}
        HAVING distance_km <= 1
        ORDER BY distance_km ASC
        LIMIT %s OFFSET %s
    """

    query_params = [lat, lon, lat] + params + [limit, offset]

    cursor.execute(query, query_params)
    rows = cursor.fetchall()

    # 컬럼명 가져오기
    colnames = [desc[0] for desc in cursor.description]

    # dict 변환
    results = [dict(zip(colnames, row)) for row in rows]

    cursor.close()
    conn.close()

    restaurants = [
        {
            "r_name": r["r_name"],
            "y": r["y"],
            "x": r["x"],
            "dong": r["dong"],
            "sort": r["sort"],
            "addr": r["addr"],
            "ads": r["ads"],
            "distance": round(r["distance_km"] * 1000),
        }
        for r in results
    ]

    return restaurants