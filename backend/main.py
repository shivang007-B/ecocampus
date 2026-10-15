from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
import logging
from backend.core.config import settings
from backend.core.database import create_tables, get_db
from backend.api.v1.api import api_router
from backend.services.iot_service import start_iot_service
import os
import random
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="""
    EcoCampus API - Real-time Carbon & GHG Tracking System for Campuses
    
    ## Features
    * Real-time campus emissions monitoring
    * Carbon footprint calculation
    * IoT device integration
    * Sustainability goal tracking
    * Green challenge management
    """,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "Something went wrong"
        }
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    logger.info("Starting EcoCampus API...")
    
    # Create database tables
    create_tables()
    logger.info("Database tables created/verified")
    
    # Auto-seed database for demo mode if needed
    try:
        from backend.core.database import SessionLocal
        from backend.models.user import User
        from backend.models.campus import Campus
        from backend.core.security import get_password_hash
        
        db = SessionLocal()
        try:
            # Seed demo admin user admin@ecocampus.com / password123
            admin_user = db.query(User).filter(User.email == 'admin@ecocampus.com').first()
            if not admin_user:
                admin_user = User(
                    email='admin@ecocampus.com',
                    username='admin',
                    full_name='Demo Admin User',
                    hashed_password=get_password_hash('password123'),
                    role='superuser',
                    is_active=True,
                    is_superuser=True
                )
                db.add(admin_user)
                db.commit()
                logger.info("Demo admin user (admin@ecocampus.com) seeded")
            
            # Seed demo campus data if empty
            has_campus = db.query(Campus).first()
            if not has_campus:
                logger.info("Seeding demo campus & emissions data...")
                setup_demo_data_sync(db)
                logger.info("Demo campus data seeded successfully")
        finally:
            db.close()
    except Exception as seed_err:
        logger.warning(f"Auto-seeding demo data failed/skipped: {seed_err}")
    
    # Serverless functions cannot maintain an MQTT connection.  The dashboard
    # still exposes seeded device telemetry in demo mode.
    if not os.getenv("VERCEL"):
        try:
            start_iot_service()
            logger.info("IoT service started")
        except Exception as e:
            logger.warning(f"Failed to start IoT service: {e}")
    
    logger.info(f"EcoCampus API started successfully - {settings.APP_NAME} v{settings.VERSION}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    logger.info("Shutting down EcoCampus API...")
    
    if not os.getenv("VERCEL"):
        from backend.services.iot_service import stop_iot_service
        stop_iot_service()
        logger.info("IoT service stopped")


from sqlalchemy import text

# Health check endpoint
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint
    """
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.VERSION,
            "database": "connected",
            "debug_mode": settings.DEBUG
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e) if settings.DEBUG else "Service unavailable"
        }, 503


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs" if settings.DEBUG else None,
        "endpoints": {
            "api": "/api/v1",
            "health": "/health",
            "auth": "/api/v1/auth",
            "campuses": "/api/v1/campuses",
            "carbon": "/api/v1/carbon",
            "iot": "/api/v1/iot"
        }
    }


def setup_demo_data_sync(db: Session):
    """
    Synchronous helper to populate demo data
    """
    from backend.services.data_service import DataService
    from backend.models.campus import Campus, Building, Department, IoTDevice
    from backend.core.security import get_password_hash
    from backend.models.user import User
    
    # Check if demo campus already exists
    existing = db.query(Campus).filter(Campus.name == "EcoCampus Demo").first()
    if not existing:
        existing = db.query(Campus).first()
        
    if existing:
        return {
            "message": "Demo campus already exists",
            "campus_id": existing.id
        }
    
    # Create demo campus
    campus = Campus(
        name="EcoCampus Demo",
        location="Green Park, Smart City",
        area_sqm=100000,
        student_count=5000,
        staff_count=500,
        building_count=5
    )
    
    db.add(campus)
    db.commit()
    db.refresh(campus)
    
    # Create demo buildings
    buildings_data = [
        {"name": "Main Academic Block", "type": "academic", "area": 20000},
        {"name": "CSE Department", "type": "academic", "area": 5000},
        {"name": "Boys Hostel A", "type": "hostel", "area": 15000},
        {"name": "Girls Hostel B", "type": "hostel", "area": 12000},
        {"name": "Central Library", "type": "library", "area": 8000},
        {"name": "Main Cafeteria", "type": "cafeteria", "area": 3000},
        {"name": "Computer Lab", "type": "lab", "area": 4000},
    ]
    
    buildings = []
    for bldg_data in buildings_data:
        building = Building(
            campus_id=campus.id,
            name=bldg_data["name"],
            building_type=bldg_data["type"],
            area_sqm=bldg_data["area"],
            floor_count=random.randint(2, 5),
            year_built=random.randint(2010, 2020),
            energy_rating=random.choice(["A", "B", "C"])
        )
        db.add(building)
        buildings.append(building)
    
    db.commit()
    
    # Create demo departments
    departments_data = [
        {"name": "Computer Science", "code": "CSE", "students": 800},
        {"name": "Electronics", "code": "ECE", "students": 600},
        {"name": "Mechanical", "code": "ME", "students": 500},
        {"name": "Mathematics", "code": "MTH", "students": 300},
        {"name": "Physics", "code": "PHY", "students": 200},
    ]
    
    for dept_data in departments_data:
        department = Department(
            campus_id=campus.id,
            name=dept_data["name"],
            code=dept_data["code"],
            student_count=dept_data["students"],
            staff_count=random.randint(20, 50),
            building_id=random.choice([b.id for b in buildings])
        )
        db.add(department)
    
    db.commit()

    # Create demo IoT devices
    iot_devices_data = [
        {"device_id": "SMART_METER_01", "name": "Academic Block Energy Meter", "type": "energy_meter", "unit": "kWh"},
        {"device_id": "WATER_SENSOR_01", "name": "Hostel Water Flow Sensor", "type": "water_meter", "unit": "liters"},
        {"device_id": "AQI_MONITOR_01", "name": "Library Air Quality Sensor", "type": "temperature_sensor", "unit": "AQI"},
        {"device_id": "WASTE_SENSOR_01", "name": "Cafeteria Waste Bin Sensor", "type": "waste_sensor", "unit": "kg"},
    ]
    for iot_data in iot_devices_data:
        device = IoTDevice(
            building_id=random.choice([b.id for b in buildings]),
            device_id=iot_data["device_id"],
            device_type=iot_data["type"],
            manufacturer="EcoTech Inc.",
            model="v1.0-Demo",
            is_active=True,
            device_metadata={"name": iot_data["name"], "unit": iot_data["unit"]}
        )
        db.add(device)
    db.commit()
    
    # Generate mock emissions data
    emissions = DataService.generate_mock_emissions(db, campus.id, days=30)
    for emission in emissions:
        db.add(emission)
    
    db.commit()
    
    # Create admin user if not exists
    admin1 = db.query(User).filter(User.email == "admin@ecocampus.com").first()
    if not admin1:
        admin1 = User(
            email="admin@ecocampus.com",
            username="admin",
            full_name="System Administrator",
            hashed_password=get_password_hash("password123"),
            role="superuser",
            is_active=True,
            is_superuser=True
        )
        db.add(admin1)

    admin2 = db.query(User).filter(User.username == "admin").first()
    if not admin2:
        admin2 = User(
            email="admin@ecocampus.edu",
            username="admin",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            role="superuser",
            is_active=True,
            is_superuser=True
        )
        db.add(admin2)

    db.commit()
    
    return {
        "message": "Demo data created successfully",
        "campus_id": campus.id,
        "campus_name": campus.name,
        "buildings_created": len(buildings),
        "departments_created": len(departments_data),
        "emissions_data": f"{len(emissions)} days",
        "admin_credentials": {
            "email": "admin@ecocampus.com",
            "password": "password123"
        }
    }

# Demo data endpoint
@app.post("/demo/setup")
async def setup_demo_data(db: Session = Depends(get_db)):
    """
    Set up demo data for testing
    """
    return setup_demo_data_sync(db)
