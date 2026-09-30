from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db import Recommendation, User
from app.models.schemas import HomeRequest, PartyRequest, JewelryRequest
from app.security import get_current_user, get_current_user_optional
from app.services.recommendation_service import generate

router = APIRouter(prefix="/api", tags=["recommendations"])

class SavePlanRequest(BaseModel):
    planner: str
    title: str
    request_data: Dict[str, Any]
    result_data: Dict[str, Any]

def save(db: Session, user: Optional[User], planner: str, p: Dict[str, Any], result: Dict[str, Any]):
    titles = {
        "home": "Home Interior Plan",
        "party": "Party Budget Plan",
        "jewelry": "Jewelry Plan"
    }
    title = titles.get(planner, f"{planner.title()} Plan")
    
    if user:
        from app.firebase_db import is_firebase_configured, fb_save_recommendation
        if is_firebase_configured():
            fb_res = fb_save_recommendation(str(user.id), planner, title, p, result)
            result["recommendation_id"] = fb_res["id"]
        else:
            r = Recommendation(
                user_id=int(user.id),
                planner=planner,
                title=title,
                request_data=p,
                result_data=result
            )
            db.add(r)
            db.commit()
            db.refresh(r)
            result["recommendation_id"] = r.id
        result["is_guest"] = False
    else:
        result["recommendation_id"] = None
        result["is_guest"] = True
        
    return result

@router.post("/generate-home")
def home(d: HomeRequest, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user_optional)):
    return save(db, user, "home", d.model_dump(), generate("home", d.model_dump()))

@router.post("/generate-party")
def party(d: PartyRequest, db: Session = Depends(get_db), user: Optional[User] = Depends(get_current_user_optional)):
    return save(db, user, "party", d.model_dump(), generate("party", d.model_dump()))

@router.post("/generate-jewelry")
async def jewelry(
    budget: float = Form(..., gt=0),
    currency: str = Form("INR"),
    occasion: str = Form(...),
    style: str = Form("elegant"),
    metal: str = Form("any"),
    outfit_description: str = Form(""),
    outfit_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    img = None
    if outfit_image and outfit_image.filename:
        if not outfit_image.content_type or not outfit_image.content_type.startswith("image/"):
            raise HTTPException(400, "outfit_image must be an image file")
        img = await outfit_image.read()
        if len(img) > 8 * 1024 * 1024:
            raise HTTPException(413, "Image must be 8 MB or smaller")

    p = JewelryRequest(
        budget=budget,
        currency=currency,
        occasion=occasion,
        style=style,
        metal=metal,
        outfit_description=outfit_description
    ).model_dump()

    return save(db, user, "jewelry", p, generate("jewelry", p, img))

@router.post("/save-recommendation")
def save_custom_plan(d: SavePlanRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    from app.firebase_db import is_firebase_configured, fb_save_recommendation
    if is_firebase_configured():
        return fb_save_recommendation(str(user.id), d.planner, d.title, d.request_data, d.result_data)
    else:
        r = Recommendation(
            user_id=int(user.id),
            planner=d.planner,
            title=d.title,
            request_data=d.request_data,
            result_data=d.result_data
        )
        db.add(r)
        db.commit()
        db.refresh(r)
        return {"id": r.id, "message": "Plan saved to dashboard successfully"}

@router.get("/recommendations-details/{rid}")
def details(rid: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    from app.firebase_db import is_firebase_configured, fb_get_recommendation
    if is_firebase_configured():
        r = fb_get_recommendation(rid, str(user.id))
        if not r:
            raise HTTPException(404, "Recommendation not found")
        return {
            "id": r["id"],
            "planner": r.get("planner"),
            "title": r.get("title"),
            "request": r.get("request_data"),
            "result": r.get("result_data"),
            "created_at": r.get("created_at")
        }
    else:
        try:
            numeric_id = int(rid)
        except ValueError:
            raise HTTPException(404, "Recommendation not found")
        r = db.get(Recommendation, numeric_id)
        if not r or r.user_id != user.id:
            raise HTTPException(404, "Recommendation not found")
        return {
            "id": r.id,
            "planner": r.planner,
            "title": r.title,
            "request": r.request_data,
            "result": r.result_data,
            "created_at": r.created_at
        }

@router.delete("/recommendations/{rid}")
def delete_recommendation(rid: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    from app.firebase_db import is_firebase_configured, fb_delete_recommendation
    if is_firebase_configured():
        success = fb_delete_recommendation(rid, str(user.id))
        if not success:
            raise HTTPException(404, "Recommendation not found")
        return {"message": "Plan deleted successfully"}
    else:
        try:
            numeric_id = int(rid)
        except ValueError:
            raise HTTPException(404, "Recommendation not found")
        r = db.get(Recommendation, numeric_id)
        if not r or r.user_id != user.id:
            raise HTTPException(404, "Recommendation not found")
        db.delete(r)
        db.commit()
        return {"message": "Plan deleted successfully"}

@router.get("/history")
def history(db: Session = Depends(get_db), user = Depends(get_current_user)):
    from app.firebase_db import is_firebase_configured, fb_get_user_history
    if is_firebase_configured():
        return fb_get_user_history(str(user.id))
    else:
        rows = db.query(Recommendation).filter(Recommendation.user_id == user.id).order_by(Recommendation.created_at.desc()).all()
        return [
            {
                "id": r.id,
                "planner": r.planner,
                "title": r.title,
                "created_at": r.created_at,
                "summary": r.result_data.get("summary", ""),
                "budget": r.result_data.get("budget", 0),
                "currency": r.result_data.get("currency", "INR")
            }
            for r in rows
        ]
