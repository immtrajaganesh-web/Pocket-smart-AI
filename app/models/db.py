from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(100))
    email: Mapped[str]=mapped_column(String(255),unique=True,index=True)
    password_hash: Mapped[str]=mapped_column(String(255))
    created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
    recommendations=relationship("Recommendation",back_populates="user",cascade="all, delete-orphan")
class Recommendation(Base):
    __tablename__="recommendations"
    id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
    planner: Mapped[str]=mapped_column(String(30))
    title: Mapped[str]=mapped_column(String(255))
    request_data: Mapped[dict]=mapped_column(JSON)
    result_data: Mapped[dict]=mapped_column(JSON)
    created_at: Mapped[datetime]=mapped_column(DateTime,default=lambda:datetime.now(timezone.utc))
    user=relationship("User",back_populates="recommendations")
