from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class CampusEmission(Base):
    __tablename__ = "campus_emissions"
    
    id = Column(Integer, primary_key=True, index=True)
    campus_id = Column(Integer, ForeignKey("campuses.id"))
    date = Column(DateTime(timezone=True), index=True, nullable=False)
    
    # Emission sources
    electricity_emission = Column(Float, default=0.0)  # kgCO2e
    transportation_emission = Column(Float, default=0.0)
    waste_emission = Column(Float, default=0.0)
    food_emission = Column(Float, default=0.0)
    water_emission = Column(Float, default=0.0)
    other_emission = Column(Float, default=0.0)
    
    # Totals
    total_emission = Column(Float, default=0.0)  # kgCO2e
    emission_per_student = Column(Float, default=0.0)  # kgCO2e/student
    emission_per_area = Column(Float, default=0.0)  # kgCO2e/sqm
    
    # Weather data
    temperature = Column(Float)
    humidity = Column(Float)
    
    # Additional data
    data_source = Column(String)  # real, simulated, manual
    notes = Column(String)
    
    # Relationships
    campus = relationship("Campus", back_populates="emissions")


class EmissionTarget(Base):
    __tablename__ = "emission_targets"
    
    id = Column(Integer, primary_key=True, index=True)
    campus_id = Column(Integer, ForeignKey("campuses.id"))
    name = Column(String, nullable=False)
    target_type = Column(String)  # absolute, intensity, reduction
    baseline_year = Column(Integer)
    target_year = Column(Integer)
    baseline_value = Column(Float)
    target_value = Column(Float)
    unit = Column(String, default="kgCO2e")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    campus = relationship("Campus")


class CarbonCredit(Base):
    __tablename__ = "carbon_credits"
    
    id = Column(Integer, primary_key=True, index=True)
    campus_id = Column(Integer, ForeignKey("campuses.id"))
    project_name = Column(String, nullable=False)
    project_type = Column(String)  # solar, wind, reforestation, efficiency
    credit_amount = Column(Float, nullable=False)  # kgCO2e
    credit_price = Column(Float)  # USD per credit
    verification_standard = Column(String)  # VER, CER, etc.
    issuance_date = Column(DateTime(timezone=True))
    expiry_date = Column(DateTime(timezone=True))
    status = Column(String, default="available")  # available, sold, retired
    credit_metadata = Column(JSON)
    
    # Relationships
    campus = relationship("Campus")


class Leaderboard(Base):
    __tablename__ = "leaderboards"
    
    id = Column(Integer, primary_key=True, index=True)
    campus_id = Column(Integer, ForeignKey("campuses.id"))
    period = Column(String)  # daily, weekly, monthly, yearly
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    
    # Top performers
    top_departments = Column(JSON)  # JSON array of department rankings
    top_buildings = Column(JSON)  # JSON array of building rankings
    top_individuals = Column(JSON)  # JSON array of individual rankings
    
    # Statistics
    total_participants = Column(Integer, default=0)
    total_carbon_saved = Column(Float, default=0.0)
    average_reduction = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    campus = relationship("Campus")