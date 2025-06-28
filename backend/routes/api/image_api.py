from flask import Blueprint, send_file, redirect
from flask_jwt_extended import jwt_required
from models import User
import io

api_image_bp = Blueprint('api_image', __name__, url_prefix='/api')

@api_image_bp.route('/images/<role>/<int:user_id>', methods=['GET'])
@jwt_required()
def get_profile_image(role, user_id):
    user = User.query.get(user_id)
    if not user or user.role != role:
        return '', 404
    if user.image:
        return send_file(
            io.BytesIO(user.image),
            mimetype=user.image_mimetype or 'image/png',
            as_attachment=False
        )
    # 역할별 기본 이미지 제공
    if role == 'mentor':
        return redirect('https://placehold.co/500x500.jpg?text=MENTOR')
    else:
        return redirect('https://placehold.co/500x500.jpg?text=MENTEE')
