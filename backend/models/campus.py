from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class Campus(Base):
    __tablename__ = "campuses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    location = Column(String)
    area_sqm = Column(Float)  # Total area in square meters
    student_count = Column(Integer)
    staff_count = Column(Integer)
    building_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    buildings = relationship("Building", back_populates="campus")
    emissions = relationship("CampusEmission", back_populates="campus")
    departments = relationship("Department", back_populates="campus")


class Building(Base):
    __tablename__ = "buildings"
    
    id = Column(Integer, primary_key=True, index=True)
    campus_id = Column(Integer, ForeignKey("campuses.id"))
    name = Column(String, nullable=False)
    building_type = Column(String)  # hostel, academic, library, cafeteria, lab, office
    area_sqm = Column(Float)
    floor_count = Column(Integer, default=1)
    year_built = Column(Integer)
    energy_rating = Column(String)  # A, B, C, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    campus = relationship("Campus", back_populates="buildings")
    iot_devices = relationship("IoTDevice", back_populates="building")


class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    campus_id = Column(Integer, ForeignKey("campuses.id"))
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True)  # e.g., CSE, ECE, ME
    student_count = Column(Integer)
    staff_count = Column(Integer)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    campus = relationship("Campus", back_populates="departments")
    building = relationship("Building")


class IoTDevice(Base):
    __tablename__ = "iot_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    device_id = Column(String, unique=True, index=True, nullable=False)
    device_type = Column(String)  # energy_meter, water_meter, waste_sensor, temperature_sensor
    manufacturer = Column(String)
    model = Column(String)
    installation_date = Column(DateTime(timezone=True))
    last_maintenance = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    device_metadata = Column(JSON)  # Additional device-specific data
    
    # Relationships
    building = relationship("Building", back_populates="iot_devices")
    readings = relationship("IoTReading", back_populates="device")


class IoTReading(Base):
    __tablename__ = "iot_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("iot_devices.id"))
    reading_type = Column(String)  # energy_kwh, water_liters, temperature_c, etc.
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Relationships
    device = relationship("IoTDevice", back_populates="readings")