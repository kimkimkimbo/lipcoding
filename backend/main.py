from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.hash import bcrypt
import jwt, datetime, os, io
from typing import List, Optional
from fastapi.responses import RedirectResponse




DATABASE_URL = "sqlite:///./mentor_mentee.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    role = Column(String)
    bio = Column(String, default="")
    skills = Column(String, default="")
    image = Column(LargeBinary, nullable=True)
    image_mimetype = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

SECRET_KEY = "your-secret-key"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(user: User):
    now = datetime.datetime.utcnow()
    payload = {
        "iss": "mentor-mentee-app",
        "sub": str(user.id),
        "aud": "mentor-mentee-client",
        "exp": now + datetime.timedelta(hours=1),
        "nbf": now,
        "iat": now,
        "jti": str(user.id) + "-" + str(now.timestamp()),
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ProfileResponse(BaseModel):
    id: int
    email: str
    role: str
    name: str
    bio: str
    skills: Optional[List[str]] = []
    imageUrl: str
    

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/swagger-ui", include_in_schema=False)
def swagger_ui():
    return RedirectResponse(url="/docs")

@app.post("/routes/api/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=req.email).first():
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    user = User(
        email=req.email,
        password_hash=bcrypt.hash(req.password),
        name=req.name,
        role=req.role,
        bio="",
        skills="" if req.role == "mentee" else "",
    )
    db.add(user)
    db.commit()
    return {"message": "Signup successful"}

@app.post("/routes/api/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=req.email).first()
    if not user or not bcrypt.verify(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user)
    return {"token": token}

@app.get("/routes/api/me", response_model=ProfileResponse)
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], audience="mentor-mentee-client")
        user = db.query(User).get(int(payload["sub"]))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return ProfileResponse(
            id=user.id, email=user.email, role=user.role, name=user.name, bio=user.bio,
            skills=user.skills.split(",") if user.skills else [],
            imageUrl=f"/api/images/{user.role}/{user.id}"
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/routes/api/mentors")
def get_mentors(skill: Optional[str] = None, orderBy: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(User).filter(User.role == "mentor")
    if skill:
        query = query.filter(User.skills.like(f"%{skill}%"))
    if orderBy == "name":
        query = query.order_by(User.name.asc())
    elif orderBy == "skill":
        query = query.order_by(User.skills.asc())
    else:
        query = query.order_by(User.id.desc())
    mentors = query.all()
    return [
        {
            "id": m.id, "email": m.email, "role": m.role,
            "profile": {
                "name": m.name, "bio": m.bio,
                "imageUrl": f"/api/images/mentor/{m.id}",
                "skills": m.skills.split(",") if m.skills else []
            }
        } for m in mentors
    ]

@app.get("/routes/api/images/{role}/{user_id}")
def get_profile_image(role: str, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user or user.role != role:
        return RedirectResponse("https://placehold.co/500x500.jpg?text=MENTOR" if role == "mentor" else "https://placehold.co/500x500.jpg?text=MENTEE")
    if user.image:
        return FileResponse(io.BytesIO(user.image), media_type=user.image_mimetype or "image/png")
    return RedirectResponse("https://placehold.co/500x500.jpg?text=MENTOR" if role == "mentor" else "https://placehold.co/500x500.jpg?text=MENTEE")

# Swagger UI: http://localhost:8080/docs
# Redoc: http://localhost:8080/redoc