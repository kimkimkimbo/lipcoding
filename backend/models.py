
# 데이터베이스 모델 정의 파일
# User, MatchRequest 모델을 정의합니다.
from db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # mentor/mentee
    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(300))
    image = db.Column(db.LargeBinary)  # 프로필 이미지 (BLOB)
    image_mimetype = db.Column(db.String(20))  # 이미지 타입
    skills = db.Column(db.String(200))  # mentor만, 콤마 구분
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class MatchRequest(db.Model):
    __tablename__ = 'match_requests'
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(300))
    status = db.Column(db.String(20), default='pending')  # pending/accepted/rejected/cancelled
    created_at = db.Column(db.DateTime, server_default=db.func.now())
