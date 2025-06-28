from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

api_user_bp = Blueprint('api_user', __name__, url_prefix='/api')

@api_user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
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
