import pandas as pd
from app_ezenfood.modules.recommend.engine.reco_rest import RestaurantRecommendationEngine
from app_ezenfood.modules.recommend.DAO.reco_dao import RecommendDAO
from app_ezenfood.modules.recommend.service.reco_service import RestaurantRecommendService
from app_ezenfood.modules.utils.get_conn import get_root_conn

"""
engine = RestaurantRecommendationEngine()

dao = RecommendDAO(get_root_conn)
conn = get_root_conn()
cursor = conn.cursor()
cursor.execute("SELECT * FROM review limit 1000")
reviews = cursor.fetchall()
cursor.execute("SELECT * FROM rest limit 100")
rests = cursor.fetchall()

cursor.close()
conn.close()
df_review = pd.DataFrame(reviews)
df_rest   = pd.DataFrame(rests)
print(df_review.info())
print(df_rest.info())
#print(reviews)
# for row in reviews :
#     df = pd.DataFrame.from_dict(row)
#     print(df.info())

#df_rest   = pd.read_csv(CSV_DIR / "filter_list.csv")
print(df_rest.columns)
print(df_rest.head())

review_stat = (
    df_review
    .groupby('rest_id')
    .agg(
        positive_reviews=('review_emotion', lambda x: (x == 1).sum()),
        total_reviews=('review_emotion', 'count')
    )
    .reset_index()
)
print(df_rest['rest_id'].dtype)
print(review_stat['rest_id'].dtype)

df_rest['positive_ratio'] = 0.7
df_rest = df_rest.merge(review_stat, on='rest_id', how='left')
df_rest[['positive_reviews','total_reviews']] = (
    df_rest[['positive_reviews','total_reviews']].fillna(0)
)
result = engine.rest_score(
    user_lat = 35.8150,
    user_lon = 127.1500,
    rest_df  = df_rest   # DAO에서 가져온 DF라고 가정
)

print(result[['rest_name', 'final_score', 'distance_km']])


df_review = pd.read_sql(
    "SELECT rest_id, review_emotion FROM review",
    con=engine2
)


print(df_review.info())
print(df_get_rest.info())
df_rest_map = (
    df_get_rest[['rest_id', 'rest_name', 'review_count']]
    .drop_duplicates(subset='rest_name')
)
print(df_rest_map.info())

df_rest = df_review.merge(
    df_rest_map,
    on  = 'rest_name',
    how = 'left'
)
print(df_rest.info())
print("+_" * 25)

result = engine.rest_score(
    user_lat = 35.8150,
    user_lon = 127.1500,
    rest_df  = df_rest   # DAO에서 가져온 DF라고 가정
)


print(result[['rest_name', 'final_score', 'distance_km']])
TRUNCATE TABLE"""



recommend = RestaurantRecommendService()
sub_id   = 1
user_lat = 35.8150
user_lon = 127.1500
print(sub_id, user_lat, user_lon)
result   = recommend.recommend_restaurants(sub_id, user_lat, user_lon)

print(result)
