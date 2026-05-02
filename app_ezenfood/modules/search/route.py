from flask import Blueprint, request, jsonify

from app_ezenfood.modules.utils.get_conn import get_conn
from app_ezenfood.modules.search.dao.sub_dao import SubDAO
from app_ezenfood.modules.search.dao.rest_dao import RestDAO
from app_ezenfood.modules.search.service import SearchService

search_bp = Blueprint("search", __name__, url_prefix="/search")

sub_dao        = SubDAO(get_conn)
rest_dao       = RestDAO(get_conn)
search_service = SearchService(sub_dao, rest_dao)

@search_bp.route("/", methods=["GET"])
def search() :
    q = request.args.get("q")
    if not q :
        return jsonify({"error" : "검색어 없음"}), 400

    result = search_service.search_sub(q)
    return jsonify(result)
