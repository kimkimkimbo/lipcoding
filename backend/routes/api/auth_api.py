from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid, datetime

from db import db
from models import User
from utils.validation import is_valid_email, is_valid_password, is_valid_name, is_valid_role

api_auth_bp = Blueprint('api_auth', __name__, url_prefix='/api')

@api_auth_bp.route('/signup', methods=['POST'])
def api_signup():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid payload'}), 400
    email = data.get('email', '').strip()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    role = data.get('role', '').strip()
    # 입력값 검증
    if not is_valid_email(email):
        return jsonify({'error': '유효한 이메일을 입력하세요.'}), 400
    if not is_valid_password(password):
        return jsonify({'error': '비밀번호는 8자 이상이어야 합니다.'}), 400
    if not is_valid_name(name):
        return jsonify({'error': '이름은 1~30자여야 합니다.'}), 400
    if not is_valid_role(role):
        return jsonify({'error': '역할은 mentor 또는 mentee만 가능합니다.'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': '이미 등록된 이메일입니다.'}), 400
    pw_hash = generate_password_hash(password, method='pbkdf2:sha256')
    user = User(email=email, password_hash=pw_hash, name=name, role=role, bio='', skills='')
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Signup successful'}), 201

@api_auth_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid payload'}), 400
    email = data.get('email', '').strip()
    password = data.get('password', '')
    if not is_valid_email(email):
        return jsonify({'error': '유효한 이메일을 입력하세요.'}), 400
    if not is_valid_password(password):
        return jsonify({'error': '비밀번호는 8자 이상이어야 합니다.'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    # JWT 표준/커스텀 클레임
    now = datetime.datetime.utcnow()
    claims = {
        'iss': 'mentor-mentee-app',
        'sub': str(user.id),
        'aud': 'mentor-mentee-client',
        'exp': now + datetime.timedelta(hours=1),
        'nbf': now,
        'iat': now,
        'jti': str(uuid.uuid4()),
        'name': user.name,
        'email': user.email,
        'role': user.role
    }
    token = create_access_token(identity=user.id, additional_claims=claims)
    return jsonify({'token': token}), 200
