from fastapi import APIRouter,Depends,HTTPException,Request,Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db import User
from app.models.schemas import RegisterRequest,LoginRequest,UserOut
from app.firebase_db import is_firebase_configured, fb_get_user_by_email, fb_create_user
from app.security import hash_password,verify_password,create_access_token,SimpleUser
router=APIRouter(prefix="/api/auth",tags=["auth"])
@router.post("/register",status_code=201)
def register(d:RegisterRequest,db:Session=Depends(get_db)):
    e=d.email.lower().strip()
    if is_firebase_configured():
        if fb_get_user_by_email(e): raise HTTPException(409,"Email is already registered")
        u=fb_create_user(name=d.name,email=e,password_hash=hash_password(d.password))
        return {"id":u["id"],"name":u["name"],"email":u["email"]}
    else:
        if db.query(User).filter(User.email==e).first(): raise HTTPException(409,"Email is already registered")
        u=User(name=d.name.strip(),email=e,password_hash=hash_password(d.password));db.add(u);db.commit();db.refresh(u);return {"id":u.id,"name":u.name,"email":u.email}
def auth(d,db):
    e=d.email.lower().strip()
    if is_firebase_configured():
        u=fb_get_user_by_email(e)
        if not u or not verify_password(d.password,u.get("password_hash","")): raise HTTPException(401,"Invalid email or password")
        return SimpleUser(u["id"],u["name"],u["email"],u.get("password_hash"))
    else:
        u=db.query(User).filter(User.email==e).first()
        if not u or not verify_password(d.password,u.password_hash): raise HTTPException(401,"Invalid email or password")
        return u
@router.post("/login")
def login(d:LoginRequest,request:Request,response:Response,db:Session=Depends(get_db)):
    u=auth(d,db)
    t=create_access_token(u.id)
    is_https = request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https"
    response.set_cookie("access_token",t,httponly=True,samesite="lax",secure=is_https,max_age=86400)
    return {"access_token":t,"token_type":"bearer","user":{"id":u.id,"name":u.name,"email":u.email}}
@router.post("/token")
def token(d:LoginRequest,db:Session=Depends(get_db)): return {"access_token":create_access_token(auth(d,db).id),"token_type":"bearer"}
@router.post("/logout")
def logout(response:Response): response.delete_cookie("access_token");return {"message":"Logged out successfully"}
