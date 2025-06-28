from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import MatchRequest, User
from utils.validation import is_valid_intro
from db import db

api_match_bp = Blueprint('api_match', __name__, url_prefix='/api')

@api_match_bp.route('/match-requests', methods=['POST'])
@jwt_required()
def create_match_request():
    data = request.get_json()
    mentor_id = data.get('mentorId')
    mentee_id = data.get('menteeId')
    message = data.get('message', '')
    # 입력값 검증
    if not mentor_id or not mentee_id:
        return jsonify({'error': '멘토/멘티 정보가 올바르지 않습니다.'}), 400
    if message and not is_valid_intro(message):
        return jsonify({'error': '요청 메시지는 1~200자여야 합니다.'}), 400
    # 멘토 존재 및 역할 확인
    mentor = User.query.get(mentor_id)
    if not mentor or mentor.role != 'mentor':
        return jsonify({'error': 'Mentor not found'}), 400
    # 멘티가 이미 대기/수락 상태의 요청이 있는지 확인(중복/동시 제한)
    existing = MatchRequest.query.filter_by(mentee_id=mentee_id).filter(MatchRequest.status.in_(['pending', 'accepted'])).first()
    if existing:
        return jsonify({'error': '이미 매칭 요청이 진행 중입니다.'}), 400
    # 동일 멘토에게 중복 요청 방지
    dup = MatchRequest.query.filter_by(mentee_id=mentee_id, mentor_id=mentor_id).filter(MatchRequest.status.in_(['pending', 'accepted'])).first()
    if dup:
        return jsonify({'error': '이미 해당 멘토에게 요청했습니다.'}), 400
    match = MatchRequest(mentor_id=mentor_id, mentee_id=mentee_id, message=message, status='pending')
    db.session.add(match)
    db.session.commit()
    return jsonify({
        'id': match.id,
        'mentorId': match.mentor_id,
        'menteeId': match.mentee_id,
        'message': match.message,
        'status': match.status
    }), 200

@api_match_bp.route('/match-requests/incoming', methods=['GET'])
@jwt_required()
def incoming_requests():
    user_id = get_jwt_identity()
    requests = MatchRequest.query.filter_by(mentor_id=user_id).all()
    return jsonify([
        {
            'id': r.id,
            'mentorId': r.mentor_id,
            'menteeId': r.mentee_id,
            'message': r.message,
            'status': r.status
        } for r in requests
    ]), 200

@api_match_bp.route('/match-requests/outgoing', methods=['GET'])
@jwt_required()
def outgoing_requests():
    user_id = get_jwt_identity()
    requests = MatchRequest.query.filter_by(mentee_id=user_id).all()
    return jsonify([
        {
            'id': r.id,
            'mentorId': r.mentor_id,
            'menteeId': r.mentee_id,
            'status': r.status
        } for r in requests
    ]), 200

@api_match_bp.route('/match-requests/<int:match_id>/accept', methods=['PUT'])
@jwt_required()
def accept_request(match_id):
    match = MatchRequest.query.get(match_id)
    if not match:
        return jsonify({'error': 'Not found'}), 404
    # 멘토가 이미 accepted 상태의 요청이 있는지 확인(1명만 수락)
    accepted = MatchRequest.query.filter_by(mentor_id=match.mentor_id, status='accepted').first()
    if accepted:
        return jsonify({'error': '이미 다른 멘티 요청을 수락 중입니다.'}), 400
    match.status = 'accepted'
    db.session.commit()
    return jsonify({
        'id': match.id,
        'mentorId': match.mentor_id,
        'menteeId': match.mentee_id,
        'message': match.message,
        'status': match.status
    }), 200

@api_match_bp.route('/match-requests/<int:match_id>/reject', methods=['PUT'])
@jwt_required()
def reject_request(match_id):
    match = MatchRequest.query.get(match_id)
    if not match:
        return jsonify({'error': 'Not found'}), 404
    match.status = 'rejected'
    db.session.commit()
    return jsonify({
        'id': match.id,
        'mentorId': match.mentor_id,
        'menteeId': match.mentee_id,
        'message': match.message,
        'status': match.status
    }), 200

@api_match_bp.route('/match-requests/<int:match_id>', methods=['DELETE'])
@jwt_required()
def delete_request(match_id):
    match = MatchRequest.query.get(match_id)
    if not match:
        return jsonify({'error': 'Not found'}), 404
    match.status = 'cancelled'
    db.session.commit()
    return jsonify({
        'id': match.id,
        'mentorId': match.mentor_id,
        'menteeId': match.mentee_id,
        'message': match.message,
        'status': match.status
    }), 200
