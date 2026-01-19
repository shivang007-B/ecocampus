from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.campus import Campus, Building, Department, IoTDevice, IoTReading
from backend.models.carbon import CampusEmission, EmissionTarget
from backend.models.user import User
from backend.schemas.campus import (
    CampusCreate,
    CampusResponse,
    CampusUpdate,
    BuildingCreate,
    BuildingResponse,
    DepartmentCreate,
    DepartmentResponse,
    IoTDeviceCreate,
    IoTDeviceResponse,
    IoTReadingCreate,
    IoTReadingResponse,
    BulkIoTReadings
)
from backend.schemas.carbon import (
    EmissionCreate,
    EmissionResponse,
    EmissionUpdate,
    EmissionTargetCreate,
    EmissionTargetResponse
)
from backend.api.v1.endpoints.auth import get_current_active_user, get_current_superuser
from backend.services.data_service import DataService
from backend.services.carbon_calculator import CarbonCalculator

router = APIRouter()


# Campus endpoints
@router.post("/", response_model=CampusResponse)
def create_campus(
    *,
    db: Session = Depends(get_db),
    campus_in: CampusCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create a new campus (admin only)
    """
    # Check if campus with same name exists
    existing = db.query(Campus).filter(Campus.name == campus_in.name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Campus with this name already exists"
        )
    
    campus = Campus(
        name=campus_in.name,
        location=campus_in.location,
        area_sqm=campus_in.area_sqm,
        student_count=campus_in.student_count,
        staff_count=campus_in.staff_count,
        building_count=campus_in.building_count
    )
    
    db.add(campus)
    db.commit()
    db.refresh(campus)
    
    # Generate mock data for the campus
    DataService.generate_mock_emissions(db, campus.id, days=30)
    
    return campus


@router.get("/", response_model=List[CampusResponse])
def read_campuses(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve all campuses
    """
    campuses = db.query(Campus).offset(skip).limit(limit).all()
    return campuses


@router.get("/{campus_id}", response_model=CampusResponse)
def read_campus(
    campus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific campus by ID
    """
    campus = db.query(Campus).filter(Campus.id == campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    return campus


@router.put("/{campus_id}", response_model=CampusResponse)
def update_campus(
    *,
    db: Session = Depends(get_db),
    campus_id: int,
    campus_in: CampusUpdate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Update a campus (admin only)
    """
    campus = db.query(Campus).filter(Campus.id == campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    update_data = campus_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(campus, field, value)
    
    db.commit()
    db.refresh(campus)
    
    return campus


@router.delete("/{campus_id}")
def delete_campus(
    campus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Delete a campus (admin only)
    """
    campus = db.query(Campus).filter(Campus.id == campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    db.delete(campus)
    db.commit()
    
    return {"message": "Campus deleted successfully"}


@router.get("/{campus_id}/dashboard")
def get_campus_dashboard(
    campus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get dashboard data for a campus
    """
    summary = DataService.get_campus_summary(db, campus_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    # Get emission trends
    trends = DataService.get_emission_trends(db, campus_id, days=7)
    
    # Get emission breakdown
    breakdown = DataService.get_emission_breakdown(db, campus_id, period="month")
    
    # Get leaderboard
    leaderboard = DataService.get_leaderboard_data(db, campus_id, period="week")
    
    return {
        "summary": summary,
        "trends": trends,
        "breakdown": breakdown,
        "leaderboard": leaderboard
    }


@router.get("/{campus_id}/summary")
def get_campus_summary(
    campus_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get summary data for a campus
    """
    summary = DataService.get_campus_summary(db, campus_id)
    
    if not summary:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    return summary


@router.get("/{campus_id}/trends")
def get_campus_trends(
    campus_id: int,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get emission trends for a campus
    """
    trends = DataService.get_emission_trends(db, campus_id, days)
    return {"campus_id": campus_id, "trends": trends}


@router.get("/{campus_id}/breakdown")
def get_campus_breakdown(
    campus_id: int,
    period: str = "month",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get emission breakdown for a campus
    """
    breakdown = DataService.get_emission_breakdown(db, campus_id, period)
    return {"campus_id": campus_id, "period": period, "breakdown": breakdown}


# Building endpoints
@router.post("/{campus_id}/buildings", response_model=BuildingResponse)
def create_building(
    *,
    db: Session = Depends(get_db),
    campus_id: int,
    building_in: BuildingCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create a new building in a campus (admin only)
    """
    # Check if campus exists
    campus = db.query(Campus).filter(Campus.id == campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    building = Building(
        campus_id=campus_id,
        name=building_in.name,
        building_type=building_in.building_type,
        area_sqm=building_in.area_sqm,
        floor_count=building_in.floor_count,
        year_built=building_in.year_built,
        energy_rating=building_in.energy_rating
    )
    
    db.add(building)
    db.commit()
    db.refresh(building)
    
    # Update campus building count
    campus.building_count = db.query(Building).filter(
        Building.campus_id == campus_id
    ).count()
    db.commit()
    
    return building


@router.get("/{campus_id}/buildings", response_model=List[BuildingResponse])
def read_buildings(
    campus_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all buildings in a campus
    """
    buildings = db.query(Building).filter(
        Building.campus_id == campus_id
    ).offset(skip).limit(limit).all()
    
    return buildings


# Department endpoints
@router.post("/{campus_id}/departments", response_model=DepartmentResponse)
def create_department(
    *,
    db: Session = Depends(get_db),
    campus_id: int,
    department_in: DepartmentCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create a new department in a campus (admin only)
    """
    # Check if campus exists
    campus = db.query(Campus).filter(Campus.id == campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    # Check if code is unique
    existing = db.query(Department).filter(Department.code == department_in.code).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Department with this code already exists"
        )
    
    department = Department(
        campus_id=campus_id,
        name=department_in.name,
        code=department_in.code,
        student_count=department_in.student_count,
        staff_count=department_in.staff_count,
        building_id=department_in.building_id
    )
    
    db.add(department)
    db.commit()
    db.refresh(department)
    
    return department


@router.get("/{campus_id}/departments", response_model=List[DepartmentResponse])
def read_departments(
    campus_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all departments in a campus
    """
    departments = db.query(Department).filter(
        Department.campus_id == campus_id
    ).offset(skip).limit(limit).all()
    
    return departments


@router.get("/{campus_id}/leaderboard")
def get_campus_leaderboard(
    campus_id: int,
    period: str = "week",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get leaderboard for a campus
    """
    leaderboard = DataService.get_leaderboard_data(db, campus_id, period)
    return leaderboard


@router.post("/{campus_id}/update-realtime")
def update_realtime_data(
    campus_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update campus with real-time data
    """
    background_tasks.add_task(DataService.update_real_time_data, db, campus_id)
    
    return {"message": "Real-time update started in background"}


@router.post("/{campus_id}/simulate")
def simulate_campus_data(
    campus_id: int,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Simulate campus data for testing (admin only)
    """
    # Generate mock emissions
    emissions = DataService.generate_mock_emissions(db, campus_id, days)
    
    # Add to database
    for emission in emissions:
        db.add(emission)
    
    db.commit()
    
    return {"message": f"Simulated {days} days of data", "records_created": len(emissions)}