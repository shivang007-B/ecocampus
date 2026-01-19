from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal


# Emission schemas
class EmissionBase(BaseModel):
    date: datetime
    
    # Emission values
    electricity_emission: Optional[float] = 0.0
    transportation_emission: Optional[float] = 0.0
    waste_emission: Optional[float] = 0.0
    food_emission: Optional[float] = 0.0
    water_emission: Optional[float] = 0.0
    other_emission: Optional[float] = 0.0
    
    # Weather
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    
    # Metadata
    data_source: Optional[str] = "simulated"
    notes: Optional[str] = None


class EmissionCreate(EmissionBase):
    campus_id: int


class EmissionUpdate(BaseModel):
    electricity_emission: Optional[float] = None
    transportation_emission: Optional[float] = None
    waste_emission: Optional[float] = None
    food_emission: Optional[float] = None
    water_emission: Optional[float] = None
    other_emission: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    notes: Optional[str] = None


class EmissionResponse(EmissionBase):
    id: int
    campus_id: int
    total_emission: float
    emission_per_student: Optional[float] = None
    emission_per_area: Optional[float] = None
    
    class Config:
        from_attributes = True


# Target schemas
class EmissionTargetBase(BaseModel):
    name: str
    target_type: str
    baseline_year: int
    target_year: int
    baseline_value: float
    target_value: float
    unit: str = "kgCO2e"


class EmissionTargetCreate(EmissionTargetBase):
    campus_id: int


class EmissionTargetResponse(EmissionTargetBase):
    id: int
    campus_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Carbon credit schemas
class CarbonCreditBase(BaseModel):
    project_name: str
    project_type: str
    credit_amount: float
    credit_price: Optional[float] = None
    verification_standard: Optional[str] = None
    issuance_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class CarbonCreditCreate(CarbonCreditBase):
    campus_id: int


class CarbonCreditResponse(CarbonCreditBase):
    id: int
    campus_id: int
    status: str
    
    class Config:
        from_attributes = True


# Leaderboard schemas
class LeaderboardBase(BaseModel):
    period: str
    period_start: datetime
    period_end: datetime


class LeaderboardCreate(LeaderboardBase):
    campus_id: int


class LeaderboardResponse(LeaderboardBase):
    id: int
    campus_id: int
    top_departments: Optional[List[Dict[str, Any]]] = None
    top_buildings: Optional[List[Dict[str, Any]]] = None
    top_individuals: Optional[List[Dict[str, Any]]] = None
    total_participants: int
    total_carbon_saved: float
    average_reduction: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard data schemas
class DashboardSummary(BaseModel):
    total_emission_today: float
    total_emission_week: float
    total_emission_month: float
    emission_change_week: float  # percentage
    emission_change_month: float  # percentage
    current_target_progress: float  # percentage
    carbon_saved_today: float
    top_saving_department: Optional[str] = None
    top_saving_building: Optional[str] = None
    active_challenges: int
    iot_devices_online: int


class EmissionTrend(BaseModel):
    date: str
    emission: float
    target: Optional[float] = None


class SourceBreakdown(BaseModel):
    source: str
    emission: float
    percentage: float


class CarbonSavingsScenario(BaseModel):
    scenario_name: str
    solar_panels_kw: Optional[float] = 0
    led_bulbs_count: Optional[int] = 0
    electric_vehicles_count: Optional[int] = 0
    waste_reduction_percent: Optional[float] = 0
    meat_reduction_percent: Optional[float] = 0
    tree_planting_count: Optional[int] = 0


class CarbonSavingsResult(BaseModel):
    scenario_name: str
    annual_savings_kg: float
    equivalent_trees: float
    equivalent_cars: float
    cost_estimation: Optional[float] = None
    payback_period_years: Optional[float] = None
    savings_breakdown: Dict[str, float]