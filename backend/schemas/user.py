from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserResponse(UserInDB):
    pass


class LoginRequest(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# Activity schemas
class ActivityBase(BaseModel):
    activity_type: str
    activity_subtype: Optional[str] = None
    value: float
    unit: str
    location: Optional[str] = None
    notes: Optional[str] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: int
    user_id: int
    carbon_emission: float
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Challenge schemas
class ChallengeBase(BaseModel):
    name: str
    description: Optional[str] = None
    challenge_type: str = "individual"
    target_value: float
    target_unit: str = "kgCO2e"
    duration_days: int = 7
    reward_points: int = 100


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeResponse(ChallengeBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserChallengeBase(BaseModel):
    challenge_id: int


class UserChallengeCreate(UserChallengeBase):
    pass


class UserChallengeResponse(UserChallengeBase):
    id: int
    user_id: int
    status: str
    progress: float
    carbon_saved: float
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True