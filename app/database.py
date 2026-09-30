import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import get_settings

settings = get_settings()
db_url = settings.database_url

# On Vercel serverless, filesystem is read-only except /tmp
is_serverless = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
if is_serverless and db_url.startswith("sqlite") and "/tmp" not in db_url:
    db_url = "sqlite:////tmp/pocketsmart.db"

# Normalise postgres:// (e.g. Supabase, Neon) to postgresql:// for SQLAlchemy
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if db_url.startswith("sqlite:///"):
    sqlite_path = db_url.replace("sqlite:///", "", 1)
    Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
class Base(DeclarativeBase): pass
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

