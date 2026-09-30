from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.database import Base,engine
from app.routers import pages,auth,session,recommendations
s=get_settings()
from app.firebase_db import init_firebase, is_firebase_configured
@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    init_firebase()
    yield
Base.metadata.create_all(bind=engine)
init_firebase()
app=FastAPI(title=s.app_name,version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=s.origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

from starlette.requests import Request
@app.middleware("http")
async def vercel_url_normalizer(request: Request, call_next):
    path = request.scope.get("path", "")
    for prefix in ("/api/index.py", "/index.py", "/main.py"):
        if path == prefix:
            request.scope["path"] = "/"
            break
        elif path.startswith(prefix + "/"):
            request.scope["path"] = path[len(prefix):]
            break
    return await call_next(request)

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(pages.router);app.include_router(auth.router);app.include_router(session.router);app.include_router(recommendations.router)
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "app": s.app_name,
        "database": "firebase-firestore" if is_firebase_configured() else "sqlite",
        "firebase_connected": is_firebase_configured(),
        "gemini_configured": bool(s.gemini_api_key),
        "model": s.gemini_model
    }
@app.get("/api/startup")
def startup():
    db_mode = "firebase-firestore" if is_firebase_configured() else "sqlite"
    return {"status":"ready","services":{"database":db_mode,"gemini":"configured" if s.gemini_api_key else "fallback-mode"}}
if __name__=="__main__":
 import uvicorn;uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
