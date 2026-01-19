from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# Campus schemas
class CampusBase(BaseModel):
    name: str
    location: Optional[str] = None
    area_sqm: Optional[float] = None
    student_count: Optional[int] = None
    staff_count: Optional[int] = None
    building_count: Optional[int] = None


class CampusCreate(CampusBase):
    pass


class CampusUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    area_sqm: Optional[float] = None
    student_count: Optional[int] = None
    staff_count: Optional[int] = None
    building_count: Optional[int] = None


class CampusResponse(CampusBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Building schemas
class BuildingBase(BaseModel):
    name: str
    building_type: str
    area_sqm: Optional[float] = None
    floor_count: Optional[int] = 1
    year_built: Optional[int] = None
    energy_rating: Optional[str] = None


class BuildingCreate(BuildingBase):
    campus_id: int


class BuildingResponse(BuildingBase):
    id: int
    campus_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Department schemas
class DepartmentBase(BaseModel):
    name: str
    code: str
    student_count: Optional[int] = None
    staff_count: Optional[int] = None


class DepartmentCreate(DepartmentBase):
    campus_id: int
    building_id: Optional[int] = None


class DepartmentResponse(DepartmentBase):
    id: int
    campus_id: int
    building_id: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# IoT schemas
class IoTDeviceBase(BaseModel):
    device_id: str
    device_type: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class IoTDeviceCreate(IoTDeviceBase):
    building_id: int


class IoTDeviceResponse(IoTDeviceBase):
    id: int
    building_id: int
    installation_date: Optional[datetime] = None
    last_maintenance: Optional[datetime] = None
    is_active: bool
    
    class Config:
        from_attributes = True


class IoTReadingBase(BaseModel):
    reading_type: str
    value: float
    unit: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class IoTReadingCreate(IoTReadingBase):
    device_id: int


class IoTReadingResponse(IoTReadingBase):
    id: int
    device_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class BulkIoTReadings(BaseModel):
    readings: List[IoTReadingCreate]