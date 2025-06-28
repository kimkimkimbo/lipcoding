import pytest
from app import app, db, initialize_database
from models import User
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

def test_mentor_list(client):
    # 멘토 2명, 멘티 1명 생성
    from werkzeug.security import generate_password_hash
    with app.app_context():
        mentor1 = User(email='m1@e.com', password_hash=generate_password_hash('pw123456', method='pbkdf2:sha256'), name='멘토1', role='mentor', bio='멘토1 소개', skills='React,Vue')
        mentor2 = User(email='m2@e.com', password_hash=generate_password_hash('pw123456', method='pbkdf2:sha256'), name='멘토2', role='mentor', bio='멘토2 소개', skills='Spring Boot,FastAPI')
        mentee = User(email='mentee@e.com', password_hash=generate_password_hash('pw123456', method='pbkdf2:sha256'), name='멘티', role='mentee', bio='멘티 소개')
        db.session.add_all([mentor1, mentor2, mentee])
        db.session.commit()
        token = get_token(mentee.id)
    # 전체 멘토 리스트
    res = client.get('/api/mentors', headers={'Authorization': f'Bearer {token}'})
    if res.status_code != 200:
        print('mentor_list 422:', res.get_json())
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) == 2
    # skill 검색
    res2 = client.get('/api/mentors?skill=React', headers={'Authorization': f'Bearer {token}'})
    assert res2.status_code == 200
    data2 = res2.get_json()
    assert len(data2) == 1
    assert data2[0]['profile']['name'] == '멘토1'
    # name 정렬
    res3 = client.get('/api/mentors?order_by=name', headers={'Authorization': f'Bearer {token}'})
    assert res3.status_code == 200
