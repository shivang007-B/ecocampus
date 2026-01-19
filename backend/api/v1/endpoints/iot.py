from typing import Any, List, Dict
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.campus import IoTDevice, IoTReading, Building
from backend.models.user import User
from backend.schemas.campus import (
    IoTDeviceCreate,
    IoTDeviceResponse,
    IoTReadingCreate,
    IoTReadingResponse,
    BulkIoTReadings
)
from backend.api.v1.endpoints.auth import get_current_active_user, get_current_superuser
from backend.services.iot_service import iot_service, IoTService
from backend.services.data_service import DataService

router = APIRouter()


# IoT Device endpoints
@router.post("/devices", response_model=IoTDeviceResponse)
def create_iot_device(
    *,
    db: Session = Depends(get_db),
    device_in: IoTDeviceCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Register a new IoT device (admin only)
    """
    # Check if building exists
    building = db.query(Building).filter(Building.id == device_in.building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Check if device ID is unique
    existing = db.query(IoTDevice).filter(IoTDevice.device_id == device_in.device_id).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Device with this ID already exists"
        )
    
    device = IoTDevice(
        building_id=device_in.building_id,
        device_id=device_in.device_id,
        device_type=device_in.device_type,
        manufacturer=device_in.manufacturer,
        model=device_in.model,
        installation_date=datetime.now(),
        last_maintenance=datetime.now(),
        is_active=True,
        metadata=device_in.metadata
    )
    
    db.add(device)
    db.commit()
    db.refresh(device)
    
    return device


@router.get("/devices", response_model=List[IoTDeviceResponse])
def read_iot_devices(
    db: Session = Depends(get_db),
    building_id: int = None,
    device_type: str = None,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve IoT devices
    """
    query = db.query(IoTDevice)
    
    if building_id:
        query = query.filter(IoTDevice.building_id == building_id)
    
    if device_type:
        query = query.filter(IoTDevice.device_type == device_type)
    
    if active_only:
        query = query.filter(IoTDevice.is_active == True)
    
    devices = query.order_by(IoTDevice.installation_date.desc()).offset(skip).limit(limit).all()
    
    return devices


@router.get("/devices/{device_id}", response_model=IoTDeviceResponse)
def read_iot_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get a specific IoT device
    """
    device = db.query(IoTDevice).filter(IoTDevice.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="IoT device not found")
    return device


@router.put("/devices/{device_id}/status")
def update_device_status(
    device_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Update IoT device status (admin only)
    """
    device = db.query(IoTDevice).filter(IoTDevice.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="IoT device not found")
    
    device.is_active = is_active
    device.last_maintenance = datetime.now()
    
    db.commit()
    
    return {"message": "Device status updated successfully"}


# IoT Reading endpoints
@router.post("/readings", response_model=IoTReadingResponse)
def create_iot_reading(
    *,
    db: Session = Depends(get_db),
    reading_in: IoTReadingCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create a new IoT reading (admin only)
    """
    # Check if device exists and is active
    device = db.query(IoTDevice).filter(
        IoTDevice.id == reading_in.device_id,
        IoTDevice.is_active == True
    ).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found or inactive")
    
    reading = IoTReading(
        device_id=reading_in.device_id,
        reading_type=reading_in.reading_type,
        value=reading_in.value,
        unit=reading_in.unit,
        timestamp=datetime.now(),
        latitude=reading_in.latitude,
        longitude=reading_in.longitude
    )
    
    db.add(reading)
    db.commit()
    db.refresh(reading)
    
    return reading


@router.post("/readings/bulk")
def create_bulk_iot_readings(
    *,
    db: Session = Depends(get_db),
    bulk_in: BulkIoTReadings,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Create multiple IoT readings at once (admin only)
    """
    readings = []
    
    for reading_in in bulk_in.readings:
        # Check if device exists and is active
        device = db.query(IoTDevice).filter(
            IoTDevice.id == reading_in.device_id,
            IoTDevice.is_active == True
        ).first()
        
        if not device:
            continue  # Skip invalid devices
        
        reading = IoTReading(
            device_id=reading_in.device_id,
            reading_type=reading_in.reading_type,
            value=reading_in.value,
            unit=reading_in.unit,
            timestamp=datetime.now(),
            latitude=reading_in.latitude,
            longitude=reading_in.longitude
        )
        
        readings.append(reading)
        db.add(reading)
    
    db.commit()
    
    return {"message": f"Created {len(readings)} readings", "count": len(readings)}


@router.get("/readings", response_model=List[IoTReadingResponse])
def read_iot_readings(
    db: Session = Depends(get_db),
    device_id: int = None,
    reading_type: str = None,
    start_time: datetime = None,
    end_time: datetime = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve IoT readings
    """
    query = db.query(IoTReading)
    
    if device_id:
        query = query.filter(IoTReading.device_id == device_id)
    
    if reading_type:
        query = query.filter(IoTReading.reading_type == reading_type)
    
    if start_time:
        query = query.filter(IoTReading.timestamp >= start_time)
    
    if end_time:
        query = query.filter(IoTReading.timestamp <= end_time)
    
    readings = query.order_by(IoTReading.timestamp.desc()).offset(skip).limit(limit).all()
    
    return readings


@router.get("/devices/{device_id}/readings/latest")
def get_latest_device_reading(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get the latest reading from a device
    """
    reading = db.query(IoTReading).filter(
        IoTReading.device_id == device_id
    ).order_by(IoTReading.timestamp.desc()).first()
    
    if not reading:
        raise HTTPException(status_code=404, detail="No readings found for this device")
    
    return reading


@router.get("/buildings/{building_id}/readings/summary")
def get_building_readings_summary(
    building_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get summary of readings for a building
    """
    # Get all devices in the building
    devices = db.query(IoTDevice).filter(
        IoTDevice.building_id == building_id,
        IoTDevice.is_active == True
    ).all()
    
    summary = {
        "building_id": building_id,
        "device_count": len(devices),
        "devices": [],
        "latest_readings": []
    }
    
    for device in devices:
        # Get latest reading for each device
        latest = db.query(IoTReading).filter(
            IoTReading.device_id == device.id
        ).order_by(IoTReading.timestamp.desc()).first()
        
        device_info = {
            "device_id": device.id,
            "device_type": device.device_type,
            "is_active": device.is_active,
            "last_maintenance": device.last_maintenance.isoformat() if device.last_maintenance else None
        }
        
        summary["devices"].append(device_info)
        
        if latest:
            summary["latest_readings"].append({
                "device_id": device.id,
                "reading_type": latest.reading_type,
                "value": latest.value,
                "unit": latest.unit,
                "timestamp": latest.timestamp.isoformat()
            })
    
    return summary


# MQTT endpoints
@router.post("/mqtt/publish")
def publish_mqtt_message(
    topic: str,
    message: str,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Publish a message to MQTT topic (admin only)
    """
    if not iot_service.is_connected:
        raise HTTPException(status_code=500, detail="MQTT service not connected")
    
    try:
        payload = json.loads(message)
    except json.JSONDecodeError:
        payload = {"message": message}
    
    iot_service.publish(topic, payload)
    
    return {"message": f"Published to {topic}", "payload": payload}


@router.get("/mqtt/status")
def get_mqtt_status() -> Any:
    """
    Get MQTT service status
    """
    return {
        "is_connected": iot_service.is_connected,
        "broker": f"{settings.MQTT_BROKER}:{settings.MQTT_PORT}",
        "subscribed_topics": [settings.MQTT_TOPIC]
    }


@router.post("/mqtt/connect")
def connect_mqtt(
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Connect to MQTT broker (admin only)
    """
    iot_service.connect()
    
    return {"message": "MQTT connection initiated"}


@router.post("/mqtt/disconnect")
def disconnect_mqtt(
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Disconnect from MQTT broker (admin only)
    """
    iot_service.disconnect()
    
    return {"message": "MQTT disconnected"}


# Simulation endpoints
@router.post("/simulate/readings")
def simulate_iot_readings(
    campus_id: int,
    count: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Simulate IoT device readings (admin only)
    """
    readings = IoTService.simulate_device_readings(db, campus_id, count)
    
    return {
        "message": f"Simulated {len(readings)} readings",
        "readings": readings
    }


@router.post("/simulate/mqtt")
def simulate_mqtt_messages(
    count: int = 5,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """
    Simulate MQTT messages (admin only)
    """
    import random
    from datetime import datetime
    
    device_types = ["energy_meter", "water_meter", "temperature_sensor", "humidity_sensor"]
    reading_types = {
        "energy_meter": ("energy_kwh", "kWh", 0.1, 10.0),
        "water_meter": ("water_liters", "liters", 100, 1000),
        "temperature_sensor": ("temperature_c", "°C", 15, 35),
        "humidity_sensor": ("humidity", "%", 30, 80),
    }
    
    messages = []
    
    for i in range(count):
        device_type = random.choice(device_types)
        reading_type, unit, min_val, max_val = reading_types[device_type]
        
        message = {
            "device_id": f"SIM_{device_type}_{i}",
            "device_type": device_type,
            "reading_type": reading_type,
            "value": round(random.uniform(min_val, max_val), 2),
            "unit": unit,
            "timestamp": datetime.now().isoformat(),
            "latitude": 26.9124 + random.uniform(-0.001, 0.001),
            "longitude": 75.7873 + random.uniform(-0.001, 0.001),
            "simulated": True
        }
        
        # Publish to MQTT
        topic = f"campus/iot/{device_type}/{i}"
        iot_service.publish(topic, message)
        
        messages.append({
            "topic": topic,
            "message": message
        })
    
    return {
        "message": f"Simulated {count} MQTT messages",
        "messages": messages
    }


# WebSocket endpoint for real-time data
@router.websocket("/ws/iot")
async def websocket_iot(websocket: WebSocket):
    """
    WebSocket endpoint for real-time IoT data
    """
    await websocket.accept()
    
    def callback(data: Dict[str, Any]):
        """
        Callback to send data through WebSocket
        """
        try:
            import asyncio
            asyncio.run(websocket.send_json(data))
        except Exception as e:
            print(f"WebSocket send error: {e}")
    
    # Add callback to IoT service
    iot_service.add_callback(callback)
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Remove callback when client disconnects
        if callback in iot_service.callbacks:
            iot_service.callbacks.remove(callback)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()