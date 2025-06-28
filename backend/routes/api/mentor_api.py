from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import User

api_mentor_bp = Blueprint('api_mentor', __name__, url_prefix='/api')

@api_mentor_bp.route('/mentors', methods=['GET'])
@jwt_required()
def get_mentors():
    # 검색/정렬 파라미터
    skill = request.args.get('skill', '').strip()
    order_by = request.args.get('order_by', '').strip()
    # 멘토만 필터
    query = User.query.filter(User.role == 'mentor')
    # 기술스택 필터
    if skill:
        query = query.filter(User.skills.ilike(f'%{skill}%'))
    # 정렬 화이트리스트
    if order_by == 'name':
        query = query.order_by(User.name.asc())
    elif order_by == 'skill':
        query = query.order_by(User.skills.asc())
    else:
        query = query.order_by(User.id.desc())
    mentors = query.all()
    result = []
    for m in mentors:
        profile = {
            'name': m.name,
            'bio': m.bio,
            'imageUrl': f"/api/images/mentor/{m.id}",
            'skills': m.skills.split(',') if m.skills else []
        }
        result.append({
            'id': m.id,
            'email': m.email,
            'role': m.role,
            'profile': profile
        })
    return jsonify(result), 200
