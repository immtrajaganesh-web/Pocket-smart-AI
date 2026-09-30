import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import get_settings
from app.database import get_db
from app.models.db import User

settings = get_settings()
oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/token", auto_error=False)

def hash_password(p: str) -> str:
    return bcrypt.hashpw(p.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(p: str, h: str) -> bool:
    try:
        return bcrypt.checkpw(p.encode('utf-8'), h.encode('utf-8'))
    except Exception:
        return False

class SimpleUser:
    def __init__(self, id, name, email, password_hash=None):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash

def create_access_token(uid: int | str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": str(uid), "exp": exp}, settings.secret_key, algorithm="HS256")

def decode_token(t: str) -> str | None:
    try:
        payload = jwt.decode(t, settings.secret_key, algorithms=["HS256"])
        return str(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError):
        return None

def get_current_user(request: Request, db: Session = Depends(get_db), bearer: str | None = Depends(oauth)) -> User | SimpleUser:
    token = bearer or request.cookies.get("access_token")
    uid = decode_token(token) if token else None
    if not uid:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    from app.firebase_db import is_firebase_configured, fb_get_user_by_id
    if is_firebase_configured():
        fb_user = fb_get_user_by_id(uid)
        if not fb_user:
            raise HTTPException(status_code=401, detail="User not found")
        return SimpleUser(fb_user["id"], fb_user["name"], fb_user["email"], fb_user.get("password_hash"))
    else:
        try:
            numeric_id = int(uid)
        except ValueError:
            raise HTTPException(status_code=401, detail="User not found")
        u = db.get(User, numeric_id)
        if not u:
            raise HTTPException(status_code=401, detail="User not found")
        return u

def get_current_user_optional(request: Request, db: Session = Depends(get_db), bearer: str | None = Depends(oauth)) -> User | SimpleUser | None:
    token = bearer or request.cookies.get("access_token")
    if not token:
        return None
    uid = decode_token(token)
    if not uid:
        return None

    from app.firebase_db import is_firebase_configured, fb_get_user_by_id
    if is_firebase_configured():
        fb_user = fb_get_user_by_id(uid)
        if not fb_user:
            return None
        return SimpleUser(fb_user["id"], fb_user["name"], fb_user["email"], fb_user.get("password_hash"))
    else:
        try:
            numeric_id = int(uid)
        except ValueError:
            return None
        return db.get(User, numeric_id)
