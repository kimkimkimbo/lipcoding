import pytest
from app import app, db, initialize_database
from models import User, MatchRequest
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        initialize_database()
        with app.test_client() as client:
            yield client
        db.drop_all()

def get_token(user_id):
    with app.app_context():
        return create_access_token(identity=str(user_id))

def test_match_request_flow(client):
    with app.app_context():
        from werkzeug.security import generate_password_hash
        mentor = User(email='mentor@e.com', password_hash=generate_password_hash('pw123456', method='pbkdf2:sha256'), name='멘토', role='mentor', bio='멘토 소개', skills='React')
        mentee = User(email='mentee@e.com', password_hash=generate_password_hash('pw123456', method='pbkdf2:sha256'), name='멘티', role='mentee', bio='멘티 소개')
        db.session.add_all([mentor, mentee])
        db.session.commit()
        mentor_token = get_token(mentor.id)
        mentee_token = get_token(mentee.id)
    # 매칭 요청 생성
    res = client.post('/api/match-requests', json={
        'mentorId': mentor.id,
        'menteeId': mentee.id,
        'message': '멘토링 받고 싶어요!'
    }, headers={'Authorization': f'Bearer {mentee_token}'})
    if res.status_code != 200:
        print('match_request 422:', res.get_json())
    assert res.status_code == 200
    # 멘토가 받은 요청 목록
    res2 = client.get('/api/match-requests/incoming', headers={'Authorization': f'Bearer {mentor_token}'})
    assert res2.status_code == 200
    data2 = res2.get_json()
    assert len(data2) == 1
    # 멘티가 보낸 요청 목록
    res3 = client.get('/api/match-requests/outgoing', headers={'Authorization': f'Bearer {mentee_token}'})
    assert res3.status_code == 200
    data3 = res3.get_json()
    assert len(data3) == 1
    # 요청 수락
    match_id = data2[0]['id']
    res4 = client.put(f'/api/match-requests/{match_id}/accept', headers={'Authorization': f'Bearer {mentor_token}'})
    assert res4.status_code == 200
    # 요청 거절
    res5 = client.put(f'/api/match-requests/{match_id}/reject', headers={'Authorization': f'Bearer {mentor_token}'})
    assert res5.status_code == 200
    # 요청 삭제
    res6 = client.delete(f'/api/match-requests/{match_id}', headers={'Authorization': f'Bearer {mentee_token}'})
    assert res6.status_code == 200
