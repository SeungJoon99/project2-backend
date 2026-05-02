from app_ezenfood.modules.search.modules.cosine_similarity import cosine_similarity as cs
import numpy as np
import json

"""
    유사도 기준 정렬 후 반환하는 함수
"""
# 매개변수 : 검색어, 카테고리 테이블의 행들, 임베딩 모델
def get_query(query, rows, model) :
    # 쿼리 임베딩
    query_emb   = model.encode([query], normalize_embeddings=True)[0]
    scored_rows = []

    for row in rows :
        # 문장 임베딩 - JSON 문자열
        sent_emb    = np.array(json.loads(row['sub_sentemb']))

        # 키워드 리스트 임베딩 - JSON 문자열
        kw_emb_list = [np.array(k) for k in json.loads(row['sub_keyemb'])]

        # 쿼리 벡터값과 문장 벡터값의 유사도
        sim_sent = cs(query_emb, sent_emb)
        
        # 키워드 리스트 임베딩에서 하나씩 꺼내서 유사도 검사 후 가장 큰 값
        sim_kw = max([cs(query_emb, kw) for kw in kw_emb_list])

        # 위 두 개 중 더 큰 것 대입
        sim = max(sim_sent, sim_kw)

        # 나온 값과 행을 리스트에 추가
        scored_rows.append((sim, row))

    # 유사도 기준 정렬
    """
        key : 
            sort의 매개변수 - 함수를 받음
            그 함수 기준으로 정렬

        람다함수 : 함수를 간단하게 줄인 것
        아래 있는 걸 복잡하게 늘리면
            def key(x) :
                return x[0]
        이렇게 됨

        sort는 기본값이 오름차순으로 나오지만 우린 가장 높은 값이 필요하기 때문에
        reverse=True를 줘서 내림차순으로 정렬
    """
    scored_rows.sort(key=lambda x: x[0], reverse=True)

    # row만 추출해서 반환
    return [row for _, row in scored_rows]


