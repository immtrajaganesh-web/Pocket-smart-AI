from fastapi import APIRouter,Depends,HTTPException,Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db import User
from app.models.schemas import RegisterRequest,LoginRequest,UserOut
from app.security import hash_password,verify_password,create_access_token
router=APIRouter(prefix="/api/auth",tags=["auth"])
@router.post("/register",response_model=UserOut,status_code=201)
def register(d:RegisterRequest,db:Session=Depends(get_db)):
    e=d.email.lower()
    if db.query(User).filter(User.email==e).first(): raise HTTPException(409,"Email is already registered")
    u=User(name=d.name.strip(),email=e,password_hash=hash_password(d.password));db.add(u);db.commit();db.refresh(u);return u
def auth(d,db):
    u=db.query(User).filter(User.email==d.email.lower()).first()
    if not u or not verify_password(d.password,u.password_hash): raise HTTPException(401,"Invalid email or password")
    return u
@router.post("/login")
def login(d:LoginRequest,response:Response,db:Session=Depends(get_db)):
    u=auth(d,db);t=create_access_token(u.id);response.set_cookie("access_token",t,httponly=True,samesite="lax",max_age=86400);return {"access_token":t,"token_type":"bearer","user":UserOut.model_validate(u).model_dump()}
@router.post("/token")
def token(d:LoginRequest,db:Session=Depends(get_db)): return {"access_token":create_access_token(auth(d,db).id),"token_type":"bearer"}
@router.post("/logout")
def logout(response:Response): response.delete_cookie("access_token");return {"message":"Logged out successfully"}
