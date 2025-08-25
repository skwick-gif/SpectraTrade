from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from models import User, Role
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from utils.notifications import send_notification

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register")
def register_user(username: str, password: str, email: str, role: str = "trader", db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    role_obj = db.query(Role).filter(Role.name == role).first()
    if not role_obj:
        role_obj = Role(name=role)
        db.add(role_obj)
        db.commit()
        db.refresh(role_obj)
    hashed = get_password_hash(password)
    user = User(username=username, hashed_password=hashed, email=email, role_id=role_obj.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    send_notification(email, f"Welcome to SpectraTrade, {username}!")
    return {"id": user.id, "username": user.username, "role": role}

@router.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": user.id, "username": user.username, "email": user.email, "role": user.role.name}

@router.get("/roles")
def list_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()