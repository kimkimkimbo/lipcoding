import pytest
from app import app, db, initialize_database
from models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        initialize_database()
        with app.test_client() as client:
            yield client
        db.drop_all()

def test_signup_and_login(client):
    # 회원가입
    res = client.post('/api/signup', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': '테스터',
        'role': 'mentor'
    })
    assert res.status_code == 201
    # 중복 회원가입
    res2 = client.post('/api/signup', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': '테스터',
        'role': 'mentor'
    })
    assert res2.status_code == 400
    # 로그인
    res3 = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert res3.status_code == 200
    assert 'token' in res3.get_json()
    # 잘못된 로그인
    res4 = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'wrongpw123'
    })
    assert res4.status_code == 401
