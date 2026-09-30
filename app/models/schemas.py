from typing import Literal, Optional, List, Dict
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    rooms: List[str] = Field(min_length=1)
    items: Dict[str, int] = Field(default_factory=dict)
    style: str = "modern"
    priorities: List[str] = Field(default_factory=list)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = "flexible"
    city: str = ""
    preferences: List[str] = Field(default_factory=list)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = "elegant"
    metal: str = "any"
    outfit_description: str = ""

class RecommendationItem(BaseModel):
    name: str
    category: str
    platform: str
    estimated_price: float
    currency: str = "INR"
    reason: str
    url: str
    tags: List[str] = Field(default_factory=list)
    rating: Optional[float] = 4.6
    badge: Optional[str] = None
    image_url: Optional[str] = None

class BudgetAllocation(BaseModel):
    category: str
    amount: float
    percentage: float

class RecommendationResponse(BaseModel):
    planner: Literal["home", "party", "jewelry"]
    summary: str
    budget: float
    currency: str
    allocations: List[BudgetAllocation] = Field(default_factory=list)
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    tips: List[str] = Field(default_factory=list)
    source_mode: Literal["gemini", "fallback"]
    disclaimer: str
    recommendation_id: Optional[int] = None
    is_guest: Optional[bool] = False
