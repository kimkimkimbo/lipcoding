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

def test_profile_update_and_get(client):
    # 회원가입 및 토큰 발급
    from werkzeug.security import generate_password_hash
    user = User(email='p@e.com', password_hash=generate_password_hash('pw123456', method='pbkdf2:sha256'), name='이름', role='mentor', bio='소개', skills='React,Vue')
    db.session.add(user)
    db.session.commit()
    token = get_token(user.id)
    # 프로필 수정
    res = client.put('/api/profile', json={
        'name': '새이름',
        'bio': '소개',
        'skills': ['React', 'Vue', 'FastAPI']
    }, headers={'Authorization': f'Bearer {token}'})
    if res.status_code != 200:
        print('profile_update 422:', res.get_json())
    assert res.status_code == 200
    # 내 정보 조회
    res2 = client.get('/api/me', headers={'Authorization': f'Bearer {token}'})
    assert res2.status_code == 200
    data = res2.get_json()
    assert data['profile']['name'] == '새이름'
