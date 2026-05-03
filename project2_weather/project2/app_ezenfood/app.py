from flask import Flask, request, render_template
from flask_cors import CORS
from app_ezenfood.modules.map_api import init_app as map_init
from pathlib import Path
from dotenv import load_dotenv
from app_ezenfood.modules.recommend.routes.router import recommend_bp
from app_ezenfood.modules.search.route import search_bp
import os
# 뭣만 하면 CSV_DIR 오류 만 하루종일 뜨길래 오류 덜뜨게 수정 완료 모듈구동법 수정함

BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "csv"

# python -m app_ezenfood.app
    
app = Flask(__name__)
CORS(app)
app.register_blueprint(recommend_bp)
app.register_blueprint(search_bp)

# 맵 init 호출
map_init(app)

app.config["CSV_DIR"] = CSV_DIR

# .env 파일 읽기
load_dotenv()
KAKAO_MAP_KEY = os.getenv("KAKAO_MAP_KEY")
# 메인 페이지   (이거 홈컨트롤 관리 말고 바로 app.py에서 렌더링 하게 수정함요)
@app.route('/')
def index():
    return render_template('map.html', kakao_key=KAKAO_MAP_KEY)

if __name__ == '__main__':
    # Render에서 제공하는 PORT 환경 변수를 읽어오고, 없으면 10000을 기본값으로 사용
    port = int(os.environ.get("PORT", 10000))
    
    print(f"서버 가동 준비 완료! (Port: {port})")
    
    # 배포 환경에서는 debug=True를 끄는 것이 좋지만, 
    # 일단 에러 확인을 위해 유지한다면 host와 port 설정을 아래처럼 바꿔야 해.
    app.run(host='0.0.0.0', port=port)




