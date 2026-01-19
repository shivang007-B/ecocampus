from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.core.database import get_db
from backend.models.carbon import CampusEmission, EmissionTarget, CarbonCredit, Leaderboard
from backend.models.campus import Campus
from backend.models.user import User
from backend.schemas.carbon import (
    EmissionCreate,
    EmissionResponse,
    EmissionUpdate,
    EmissionTargetCreate,
    EmissionTargetResponse,
    CarbonCreditCreate,
    CarbonCreditResponse,
    LeaderboardCreate,
    LeaderboardResponse,
    CarbonSavingsScenario,
    CarbonSavingsResult,
    DashboardSummary
)
from backend.api.v1.endpoints.auth import get_current_active_user, get_current_superuser
from backend.services.carbon_calculator import CarbonCalculator
from backend.services.data_service import DataService
from backend.utils.helpers import calculate_carbon_savings

router = APIRouter()


# Emission endpoints
@router.post("/emissions", response_model=EmissionResponse)
def create_emission(
    *,
    db: Session = Depends(get_db),
    emission_in: EmissionCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create a new emission record (admin only)
    """
    # Check if campus exists
    campus = db.query(Campus).filter(Campus.id == emission_in.campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    # Calculate totals
    total_emission = (
        emission_in.electricity_emission +
        emission_in.transportation_emission +
        emission_in.waste_emission +
        emission_in.food_emission +
        emission_in.water_emission +
        emission_in.other_emission
    )
    
    # Calculate intensity metrics
    emission_per_student = None
    emission_per_area = None
    
    if campus.student_count and campus.student_count > 0:
        emission_per_student = total_emission / campus.student_count
    
    if campus.area_sqm and campus.area_sqm > 0:
        emission_per_area = total_emission / campus.area_sqm
    
    emission = CampusEmission(
        campus_id=emission_in.campus_id,
        date=emission_in.date,
        electricity_emission=emission_in.electricity_emission,
        transportation_emission=emission_in.transportation_emission,
        waste_emission=emission_in.waste_emission,
        food_emission=emission_in.food_emission,
        water_emission=emission_in.water_emission,
        other_emission=emission_in.other_emission,
        total_emission=total_emission,
        emission_per_student=emission_per_student,
        emission_per_area=emission_per_area,
        temperature=emission_in.temperature,
        humidity=emission_in.humidity,
        data_source=emission_in.data_source,
        notes=emission_in.notes
    )
    
    db.add(emission)
    db.commit()
    db.refresh(emission)
    
    return emission


@router.get("/emissions", response_model=List[EmissionResponse])
def read_emissions(
    db: Session = Depends(get_db),
    campus_id: int = None,
    start_date: datetime = None,
    end_date: datetime = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve emissions with optional filters
    """
    query = db.query(CampusEmission)
    
    if campus_id:
        query = query.filter(CampusEmission.campus_id == campus_id)
    
    if start_date:
        query = query.filter(CampusEmission.date >= start_date)
    
    if end_date:
        query = query.filter(CampusEmission.date <= end_date)
    
    emissions = query.order_by(CampusEmission.date.desc()).offset(skip).limit(limit).all()
    
    return emissions


@router.get("/emissions/{emission_id}", response_model=EmissionResponse)
def read_emission(
    emission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific emission record
    """
    emission = db.query(CampusEmission).filter(CampusEmission.id == emission_id).first()
    if not emission:
        raise HTTPException(status_code=404, detail="Emission record not found")
    return emission


@router.put("/emissions/{emission_id}", response_model=EmissionResponse)
def update_emission(
    *,
    db: Session = Depends(get_db),
    emission_id: int,
    emission_in: EmissionUpdate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Update an emission record (admin only)
    """
    emission = db.query(CampusEmission).filter(CampusEmission.id == emission_id).first()
    if not emission:
        raise HTTPException(status_code=404, detail="Emission record not found")
    
    # Get current values to recalculate total
    update_data = emission_in.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(emission, field, value)
    
    # Recalculate total
    emission.total_emission = (
        emission.electricity_emission +
        emission.transportation_emission +
        emission.waste_emission +
        emission.food_emission +
        emission.water_emission +
        emission.other_emission
    )
    
    # Recalculate intensity metrics
    campus = db.query(Campus).filter(Campus.id == emission.campus_id).first()
    if campus:
        if campus.student_count and campus.student_count > 0:
            emission.emission_per_student = emission.total_emission / campus.student_count
        
        if campus.area_sqm and campus.area_sqm > 0:
            emission.emission_per_area = emission.total_emission / campus.area_sqm
    
    db.commit()
    db.refresh(emission)
    
    return emission


@router.delete("/emissions/{emission_id}")
def delete_emission(
    emission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Delete an emission record (admin only)
    """
    emission = db.query(CampusEmission).filter(CampusEmission.id == emission_id).first()
    if not emission:
        raise HTTPException(status_code=404, detail="Emission record not found")
    
    db.delete(emission)
    db.commit()
    
    return {"message": "Emission record deleted successfully"}


@router.get("/campus/{campus_id}/emissions/today")
def get_today_emission(
    campus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get today's emission for a campus
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    emission = db.query(CampusEmission).filter(
        CampusEmission.campus_id == campus_id,
        CampusEmission.date >= today,
        CampusEmission.date < today + timedelta(days=1)
    ).first()
    
    if not emission:
        # Return default if no data for today
        return {
            "campus_id": campus_id,
            "date": today.isoformat(),
            "total_emission": 0,
            "has_data": False
        }
    
    return emission


@router.get("/campus/{campus_id}/emissions/period")
def get_emissions_period(
    campus_id: int,
    period: str = "week",  # day, week, month, year
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get emissions for a specific period
    """
    end_date = datetime.now()
    
    if period == "day":
        start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start_date = end_date - timedelta(days=7)
    elif period == "month":
        start_date = end_date - timedelta(days=30)
    elif period == "year":
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)
    
    emissions = db.query(CampusEmission).filter(
        CampusEmission.campus_id == campus_id,
        CampusEmission.date >= start_date,
        CampusEmission.date <= end_date
    ).order_by(CampusEmission.date).all()
    
    total = sum(e.total_emission for e in emissions)
    average = total / len(emissions) if emissions else 0
    
    return {
        "campus_id": campus_id,
        "period": period,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "total_emission": total,
        "average_daily": average,
        "emission_count": len(emissions),
        "emissions": emissions
    }


# Emission target endpoints
@router.post("/targets", response_model=EmissionTargetResponse)
def create_emission_target(
    *,
    db: Session = Depends(get_db),
    target_in: EmissionTargetCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create a new emission target (admin only)
    """
    # Check if campus exists
    campus = db.query(Campus).filter(Campus.id == target_in.campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    target = EmissionTarget(
        campus_id=target_in.campus_id,
        name=target_in.name,
        target_type=target_in.target_type,
        baseline_year=target_in.baseline_year,
        target_year=target_in.target_year,
        baseline_value=target_in.baseline_value,
        target_value=target_in.target_value,
        unit=target_in.unit,
        is_active=True
    )
    
    db.add(target)
    db.commit()
    db.refresh(target)
    
    return target


@router.get("/targets", response_model=List[EmissionTargetResponse])
def read_emission_targets(
    db: Session = Depends(get_db),
    campus_id: int = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve emission targets
    """
    query = db.query(EmissionTarget)
    
    if campus_id:
        query = query.filter(EmissionTarget.campus_id == campus_id)
    
    if active_only:
        query = query.filter(EmissionTarget.is_active == True)
    
    targets = query.order_by(EmissionTarget.created_at.desc()).offset(skip).limit(limit).all()
    
    return targets


@router.put("/targets/{target_id}/status")
def update_target_status(
    target_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Update emission target status (admin only)
    """
    target = db.query(EmissionTarget).filter(EmissionTarget.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    
    target.is_active = is_active
    db.commit()
    
    return {"message": "Target status updated successfully"}


# Carbon credit endpoints
@router.post("/credits", response_model=CarbonCreditResponse)
def create_carbon_credit(
    *,
    db: Session = Depends(get_db),
    credit_in: CarbonCreditCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create a new carbon credit (admin only)
    """
    # Check if campus exists
    campus = db.query(Campus).filter(Campus.id == credit_in.campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    credit = CarbonCredit(
        campus_id=credit_in.campus_id,
        project_name=credit_in.project_name,
        project_type=credit_in.project_type,
        credit_amount=credit_in.credit_amount,
        credit_price=credit_in.credit_price,
        verification_standard=credit_in.verification_standard,
        issuance_date=credit_in.issuance_date,
        expiry_date=credit_in.expiry_date,
        status="available",
        metadata=credit_in.metadata
    )
    
    db.add(credit)
    db.commit()
    db.refresh(credit)
    
    return credit


@router.get("/credits", response_model=List[CarbonCreditResponse])
def read_carbon_credits(
    db: Session = Depends(get_db),
    campus_id: int = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve carbon credits
    """
    query = db.query(CarbonCredit)
    
    if campus_id:
        query = query.filter(CarbonCredit.campus_id == campus_id)
    
    if status:
        query = query.filter(CarbonCredit.status == status)
    
    credits = query.order_by(CarbonCredit.issuance_date.desc()).offset(skip).limit(limit).all()
    
    return credits


# Analysis endpoints
@router.post("/campus/{campus_id}/analyze/savings")
def analyze_savings(
    campus_id: int,
    scenario: CarbonSavingsScenario,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Analyze potential carbon savings for a scenario
    """
    # Convert scenario to dict
    scenario_dict = scenario.dict()
    
    # Calculate savings
    result = DataService.calculate_savings_scenario(db, campus_id, scenario_dict)
    
    return CarbonSavingsResult(
        scenario_name=scenario.scenario_name,
        annual_savings_kg=result["total_reduction_kg"],
        equivalent_trees=result["equivalent_trees"],
        equivalent_cars=result["equivalent_cars"],
        cost_estimation=result.get("total_cost"),
        payback_period_years=result.get("payback_years"),
        savings_breakdown=result["reduction_breakdown"]
    )


@router.post("/calculate/direct")
def calculate_direct_emission(
    electricity_kwh: float = 0,
    transport_data: str = None,
    waste_kg: float = 0,
    meals_data: str = None,
    water_liters: float = 0,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Calculate direct carbon emissions
    """
    calculator = CarbonCalculator()
    
    # Parse transport data
    transport_dict = {}
    if transport_data:
        try:
            import json
            transport_dict = json.loads(transport_data)
        except:
            # Try comma-separated format: "car:100,bus:50"
            for item in transport_data.split(','):
                if ':' in item:
                    mode, distance = item.split(':')
                    transport_dict[mode.strip()] = float(distance.strip())
    
    # Parse meals data
    meals_dict = {}
    if meals_data:
        try:
            import json
            meals_dict = json.loads(meals_data)
        except:
            # Try comma-separated format: "beef:2,vegetarian:5"
            for item in meals_data.split(','):
                if ':' in item:
                    meal_type, count = item.split(':')
                    meals_dict[meal_type.strip()] = int(count.strip())
    
    # Calculate emissions
    result = calculator.calculate_total_campus_emission(
        electricity_kwh=electricity_kwh,
        transport_data=transport_dict,
        waste_data={"general": waste_kg},
        meals_data=meals_dict,
        water_liters=water_liters
    )
    
    return result


@router.get("/campus/{campus_id}/dashboard-summary")
def get_dashboard_summary(
    campus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get dashboard summary for a campus
    """
    summary = DataService.get_campus_summary(db, campus_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    # Get emissions for today and yesterday for comparison
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    today_emission = db.query(CampusEmission).filter(
        CampusEmission.campus_id == campus_id,
        CampusEmission.date >= today,
        CampusEmission.date < today + timedelta(days=1)
    ).first()
    
    yesterday_emission = db.query(CampusEmission).filter(
        CampusEmission.campus_id == campus_id,
        CampusEmission.date >= yesterday,
        CampusEmission.date < yesterday + timedelta(days=1)
    ).first()
    
    # Calculate change
    emission_today = today_emission.total_emission if today_emission else 0
    emission_yesterday = yesterday_emission.total_emission if yesterday_emission else 0
    
    if emission_yesterday > 0:
        change_percent = ((emission_today - emission_yesterday) / emission_yesterday) * 100
    else:
        change_percent = 0
    
    # Get active targets progress
    targets = db.query(EmissionTarget).filter(
        EmissionTarget.campus_id == campus_id,
        EmissionTarget.is_active == True
    ).all()
    
    target_progress = 0
    if targets:
        # Simple average of all targets
        progresses = []
        for target in targets:
            progress = min(100, (target.baseline_value - summary["month_emission"]) / target.baseline_value * 100)
            progresses.append(max(0, progress))
        
        target_progress = sum(progresses) / len(progresses) if progresses else 0
    
    # Get IoT device count (simulated for now)
    from backend.models.campus import IoTDevice
    iot_count = db.query(IoTDevice).filter(
        IoTDevice.building_id.in_(
            db.query(Building.id).filter(Building.campus_id == campus_id)
        )
    ).count()
    
    return DashboardSummary(
        total_emission_today=emission_today,
        total_emission_week=summary["week_emission"],
        total_emission_month=summary["month_emission"],
        emission_change_week=round(change_percent, 2),
        emission_change_month=0,  # Would need more data
        current_target_progress=round(target_progress, 2),
        carbon_saved_today=0,  # Would need activity data
        top_saving_department="CSE",  # Mock data
        top_saving_building="Main Building",  # Mock data
        active_challenges=summary["active_targets"],
        iot_devices_online=iot_count
    )