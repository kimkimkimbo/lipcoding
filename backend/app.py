
# ================================
# Flask 메인 서버 진입점 (최적화/중복 제거)
# ================================
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, send_file
from flasgger import Swagger
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from db import db


# Flask 앱 및 확장 초기화
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mentor_mentee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 확장 등록
swagger = Swagger(app, template_file="../openapi.yaml")
CORS(app)
jwt = JWTManager(app)
db.init_app(app)

# DB 자동 초기화 함수 (서버/테스트 모두에서 명시적으로 호출)
def initialize_database():
    from models import User, MatchRequest
    with app.app_context():
        db.create_all()

# REST API 블루프린트 등록
from routes.api.auth_api import api_auth_bp
from routes.api.user_api import api_user_bp
from routes.api.mentor_api import api_mentor_bp
from routes.api.image_api import api_image_bp
from routes.api.profile_api import api_profile_bp
from routes.api.match_api import api_match_bp
app.register_blueprint(api_auth_bp)
app.register_blueprint(api_user_bp)
app.register_blueprint(api_mentor_bp)
app.register_blueprint(api_image_bp)
app.register_blueprint(api_profile_bp)
app.register_blueprint(api_match_bp)

# Swagger/OpenAPI 문서 제공
@app.route("/openapi.json")
def openapi_json():
    # 미사용 코드 제거: openapi.yaml 파싱 및 반환 생략
    return "Not Implemented", 501

@app.route("/swagger-ui")
def swagger_ui():
    return redirect("/apidocs")

@app.route("/")
def root():
    return redirect("/swagger-ui")

if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=8080, debug=True)
