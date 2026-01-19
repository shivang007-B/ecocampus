from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.user import User, UserActivity, Challenge, UserChallenge
from backend.schemas.user import (
    UserResponse,
    ActivityCreate,
    ActivityResponse,
    ChallengeCreate,
    ChallengeResponse,
    UserChallengeCreate,
    UserChallengeResponse
)
from backend.api.v1.endpoints.auth import get_current_active_user, get_current_superuser
from backend.services.carbon_calculator import CarbonCalculator

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Retrieve users (admin only)
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Get a specific user by ID (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Delete a user (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}


@router.post("/activities", response_model=ActivityResponse)
def create_activity(
    *,
    db: Session = Depends(get_db),
    activity_in: ActivityCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create a new user activity
    """
    # Calculate carbon emission
    calculator = CarbonCalculator()
    carbon_emission = 0.0
    
    if activity_in.activity_type == "transport":
        if activity_in.activity_subtype:
            transport_data = {activity_in.activity_subtype: activity_in.value}
            result = calculator.calculate_transport_emission(transport_data)
            carbon_emission = result["total_emission_kg"]
    
    elif activity_in.activity_type == "food":
        if activity_in.activity_subtype:
            meals_data = {activity_in.activity_subtype: int(activity_in.value)}
            result = calculator.calculate_food_emission(meals_data)
            carbon_emission = result["total_emission_kg"]
    
    elif activity_in.activity_type == "energy":
        carbon_emission = calculator.calculate_electricity_emission(activity_in.value)
    
    elif activity_in.activity_type == "waste":
        waste_data = {"general": activity_in.value}
        result = calculator.calculate_waste_emission(waste_data)
        carbon_emission = result["total_emission_kg"]
    
    # Create activity
    activity = UserActivity(
        user_id=current_user.id,
        activity_type=activity_in.activity_type,
        activity_subtype=activity_in.activity_subtype,
        value=activity_in.value,
        unit=activity_in.unit,
        carbon_emission=carbon_emission,
        location=activity_in.location,
        notes=activity_in.notes
    )
    
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return activity


@router.get("/activities/me", response_model=List[ActivityResponse])
def read_my_activities(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user's activities
    """
    activities = db.query(UserActivity).filter(
        UserActivity.user_id == current_user.id
    ).order_by(UserActivity.timestamp.desc()).offset(skip).limit(limit).all()
    
    return activities


@router.get("/activities/summary")
def get_activities_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get summary of user's activities and carbon footprint
    """
    activities = db.query(UserActivity).filter(
        UserActivity.user_id == current_user.id
    ).all()
    
    total_emission = sum(a.carbon_emission for a in activities)
    
    # Group by activity type
    by_type = {}
    for activity in activities:
        if activity.activity_type not in by_type:
            by_type[activity.activity_type] = {
                "count": 0,
                "total_emission": 0.0
            }
        
        by_type[activity.activity_type]["count"] += 1
        by_type[activity.activity_type]["total_emission"] += activity.carbon_emission
    
    # Calculate daily average (last 30 days)
    from datetime import datetime, timedelta
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    recent_activities = db.query(UserActivity).filter(
        UserActivity.user_id == current_user.id,
        UserActivity.timestamp >= thirty_days_ago
    ).all()
    
    recent_emission = sum(a.carbon_emission for a in recent_activities)
    daily_average = recent_emission / 30 if recent_activities else 0
    
    return {
        "total_activities": len(activities),
        "total_carbon_emission_kg": total_emission,
        "daily_average_kg": daily_average,
        "breakdown_by_type": by_type,
        "equivalent_trees": total_emission / 21.77,  # Trees needed to absorb
        "equivalent_car_km": total_emission / 0.192,  # Petrol car emissions per km
    }


@router.post("/challenges", response_model=ChallengeResponse)
def create_challenge(
    *,
    db: Session = Depends(get_db),
    challenge_in: ChallengeCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create a new challenge (admin only)
    """
    challenge = Challenge(
        name=challenge_in.name,
        description=challenge_in.description,
        challenge_type=challenge_in.challenge_type,
        target_value=challenge_in.target_value,
        target_unit=challenge_in.target_unit,
        duration_days=challenge_in.duration_days,
        reward_points=challenge_in.reward_points,
        is_active=True
    )
    
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    
    return challenge


@router.get("/challenges", response_model=List[ChallengeResponse])
def read_challenges(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all challenges
    """
    query = db.query(Challenge)
    
    if active_only:
        query = query.filter(Challenge.is_active == True)
    
    challenges = query.order_by(Challenge.created_at.desc()).offset(skip).limit(limit).all()
    
    return challenges


@router.post("/challenges/join", response_model=UserChallengeResponse)
def join_challenge(
    *,
    db: Session = Depends(get_db),
    challenge_in: UserChallengeCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Join a challenge
    """
    # Check if challenge exists and is active
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_in.challenge_id,
        Challenge.is_active == True
    ).first()
    
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found or inactive")
    
    # Check if already joined
    existing = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.challenge_id == challenge_in.challenge_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already joined this challenge")
    
    # Join challenge
    user_challenge = UserChallenge(
        user_id=current_user.id,
        challenge_id=challenge_in.challenge_id,
        status="active",
        progress=0.0,
        carbon_saved=0.0
    )
    
    db.add(user_challenge)
    db.commit()
    db.refresh(user_challenge)
    
    return user_challenge


@router.get("/challenges/my", response_model=List[UserChallengeResponse])
def read_my_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user's challenges
    """
    user_challenges = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id
    ).all()
    
    return user_challenges


@router.post("/challenges/{challenge_id}/update")
def update_challenge_progress(
    challenge_id: int,
    progress: float,
    carbon_saved: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update challenge progress
    """
    user_challenge = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.challenge_id == challenge_id
    ).first()
    
    if not user_challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    user_challenge.progress = progress
    user_challenge.carbon_saved = carbon_saved
    
    if progress >= 100 and user_challenge.status == "active":
        user_challenge.status = "completed"
        user_challenge.completed_at = datetime.now()
    
    db.commit()
    
    return {"message": "Progress updated successfully"}