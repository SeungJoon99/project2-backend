from sentence_transformers import SentenceTransformer
from app_ezenfood.modules.search.dao.sub_dao import SubDAO
from app_ezenfood.modules.search.dao.rest_dao import RestDAO
from app_ezenfood.modules.search.modules.get_query import get_query
import json


class SearchService :
    # 여기서 :(콜론)의 의미 : 
    #   타입 힌트 - x : dao - x라는 변수에는 dao라는 타입이 들어올 예정
    #   강제성은 없다. 말 그대로 힌트
    def __init__(self, sub_dao : SubDAO, rest_dao : RestDAO) :
        self.sub_dao  = sub_dao
        self.rest_dao = rest_dao
        self.model    = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")

    def search_sub(self, query) :
        rows        = self.sub_dao.fetch_all()
        sorted_subs = get_query(query, rows, self.model)[:3]

        rests = {}
        for sub in sorted_subs :
            name = sub['sub_name']
            id   = sub['sub_id']
            rests[name] = self.rest_dao.select_by_sub(id)[:5]

        return {"subs": sorted_subs, "rests": rests}

class SubEmbedding :
    def __init__(self) :
        self.model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")

    def insert_sub(self, categories) :
        sentences = [sentence for name, sentence, keys in categories]
        sentence_embeddings = self.model.encode(sentences, normalize_embeddings=True)

        all_key_embs = [
            self.model.encode(keys, normalize_embeddings=True)
            for name, sentence, keys in categories
        ]

        data_list = []
        for (name, sentence, keys), sent_emb, key_embs in zip(categories, sentence_embeddings, all_key_embs) :
            key_embs_list = [emb.tolist() for emb in key_embs]
            data_list.append((
                name,
                sentence,
                json.dumps(sent_emb.tolist()),
                json.dumps(keys),
                json.dumps(key_embs_list)
            ))

        SubDAO.insert(data_list)
        print(f"{len(data_list)}개 삽입 완료")

