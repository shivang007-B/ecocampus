from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # user, admin, superuser
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    activities = relationship("UserActivity", back_populates="user")
    challenges = relationship("UserChallenge", back_populates="user")


class UserActivity(Base):
    __tablename__ = "user_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_type = Column(String, nullable=False)  # transport, food, energy, waste
    activity_subtype = Column(String)  # car, bike, beef, chicken, etc.
    value = Column(Float, nullable=False)  # km, kg, kWh, etc.
    unit = Column(String, nullable=False)
    carbon_emission = Column(Float, nullable=False)  # kgCO2e
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    location = Column(String)  # Optional location data
    notes = Column(String)  # Optional notes
    
    # Relationships
    user = relationship("User", back_populates="activities")


class UserChallenge(Base):
    __tablename__ = "user_challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    status = Column(String, default="active")  # active, completed, failed
    progress = Column(Float, default=0.0)  # 0-100 percentage
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    carbon_saved = Column(Float, default=0.0)  # kgCO2e saved
    
    # Relationships
    user = relationship("User", back_populates="challenges")
    challenge = relationship("Challenge", back_populates="participants")


class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    challenge_type = Column(String)  # individual, team, campus
    target_value = Column(Float, nullable=False)  # Target carbon saving
    target_unit = Column(String, default="kgCO2e")
    duration_days = Column(Integer, default=7)
    reward_points = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    participants = relationship("UserChallenge", back_populates="challenge")