from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db import User,Recommendation
from app.models.schemas import UserOut
from app.security import get_current_user
from app.firebase_db import is_firebase_configured, fb_get_user_history
router=APIRouter(prefix="/api",tags=["session"])
@router.get("/session-info")
def info(request:Request,user=Depends(get_current_user)): return {"authenticated":True,"user_id":user.id,"email":user.email,"session_cookie":bool(request.cookies.get("access_token"))}
@router.get("/session-data")
def data(db:Session=Depends(get_db),user=Depends(get_current_user)):
    if is_firebase_configured():
        count = len(fb_get_user_history(str(user.id)))
    else:
        count = db.query(Recommendation).filter(Recommendation.user_id==user.id).count()
    return {"user":{"id":user.id,"name":user.name,"email":user.email},"recommendation_count":count}
