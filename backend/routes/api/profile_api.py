from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
import base64
from utils.image_validation import validate_profile_image
from utils.validation import is_valid_name, is_valid_intro, is_valid_stack
from db import db

api_profile_bp = Blueprint('api_profile', __name__, url_prefix='/api')

# 프로필 조회
@api_profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 401
    profile = {
        'name': user.name,
        'bio': user.bio,
        'imageUrl': f"/api/images/{user.role}/{user.id}",
    }
    if user.role == 'mentor':
        profile['skills'] = user.skills.split(',') if user.skills else []
    return jsonify({
        'id': user.id,
        'email': user.email,
        'role': user.role,
        'profile': profile
    }), 200

# 프로필 수정
@api_profile_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 401
    data = request.get_json()
    # 이름 검증
    name = data.get('name', user.name)
    if not is_valid_name(name):
        return jsonify({'error': '이름은 1~30자여야 합니다.'}), 400
    user.name = name
    # 소개글 검증
    bio = data.get('bio', user.bio)
    if not is_valid_intro(bio):
        return jsonify({'error': '소개글은 1~200자여야 합니다.'}), 400
    user.bio = bio
    # 이미지 검증
    if 'image' in data and data['image']:
        try:
            image_bytes = base64.b64decode(data['image'])
            from werkzeug.datastructures import FileStorage
            import io
            file_storage = FileStorage(stream=io.BytesIO(image_bytes), filename='profile.png', content_type='image/png')
            valid, msg = validate_profile_image(file_storage)
            if not valid:
                return jsonify({'error': msg}), 400
            user.image = image_bytes
            user.image_mimetype = 'image/png'
        except Exception:
            return jsonify({'error': 'Invalid image encoding'}), 400
    # 멘토 skills 검증
    if user.role == 'mentor':
        skills = data.get('skills', [])
        skills_str = ','.join(skills)
        if not is_valid_stack(skills_str):
            return jsonify({'error': '기술스택은 각 항목 1~20자, 전체 100자 이하, 최소 1개여야 합니다.'}), 400
        user.skills = skills_str
    db.session.commit()
    profile = {
        'name': user.name,
        'bio': user.bio,
        'imageUrl': f"/api/images/{user.role}/{user.id}",
    }
    if user.role == 'mentor':
        profile['skills'] = user.skills.split(',') if user.skills else []
    return jsonify({
        'id': user.id,
        'email': user.email,
        'role': user.role,
        'profile': profile
    }), 200
