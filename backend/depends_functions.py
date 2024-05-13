from fastapi import HTTPException, status, Header
from database.engin import SessionLocal
from database import models 
from settings import *
import string
import secrets
import uuid

session = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def commitData(date,db):
    db.add(date)
    db.commit()
    db.refresh(date)
    return True

def generate_token(length=30):
    allowed_characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(allowed_characters) for _ in range(length))
    return token

def check_token(token):
    user = session.query(models.Users).filter(models.Users.token == token).first()
    if user : return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Username Not Exists"
    )

def auth_authz(permission: list = []):
    def _auth_authz(token: str = Header(...)):
        user = check_token(token)
        if permission[0] != 'all' and user.role not in permission:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This Account Does Not Have Permission"
            )
        return user
    return _auth_authz

def check_user(email, db):
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if user:
        return user
    return None

def generate_random_media_name(length=10, extension=".png"):
    random_name = str(uuid.uuid4())
    random_part = random_name[:length]
    if not extension.startswith("."):
        extension = "." + extension
    return random_part + extension