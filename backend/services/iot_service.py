"""
IoT Service for handling device data
"""
import json
import paho.mqtt.client as mqtt
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import threading
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.models.campus import IoTDevice, IoTReading
from backend.schemas.campus import IoTReadingCreate


class IoTService:
    """
    MQTT-based IoT service for real-time device data
    """
    
    def __init__(self):
        self.client = None
        self.callbacks = []
        self.is_connected = False
        self.device_cache = {}
    
    def connect(self):
        """
        Connect to MQTT broker
        """
        if self.is_connected:
            return
        
        self.client = mqtt.Client(client_id=f"ecocampus_{datetime.now().timestamp()}")
        
        # Set up callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        
        try:
            self.client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
            self.client.loop_start()
            self.is_connected = True
            print(f"Connected to MQTT broker at {settings.MQTT_BROKER}:{settings.MQTT_PORT}")
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            self.is_connected = False
    
    def disconnect(self):
        """
        Disconnect from MQTT broker
        """
        if self.client and self.is_connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.is_connected = False
    
    def subscribe(self, topic: str):
        """
        Subscribe to MQTT topic
        """
        if self.client and self.is_connected:
            self.client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")
    
    def publish(self, topic: str, payload: Dict[str, Any]):
        """
        Publish message to MQTT topic
        """
        if self.client and self.is_connected:
            self.client.publish(topic, json.dumps(payload))
    
    def add_callback(self, callback: Callable):
        """
        Add callback for received messages
        """
        self.callbacks.append(callback)
    
    def _on_connect(self, client, userdata, flags, rc):
        """
        MQTT connection callback
        """
        if rc == 0:
            print("MQTT connection successful")
            # Subscribe to default topic
            self.subscribe(settings.MQTT_TOPIC)
        else:
            print(f"MQTT connection failed with code: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """
        MQTT message received callback
        """
        try:
            payload = json.loads(msg.payload.decode())
            
            # Add timestamp if not present
            if "timestamp" not in payload:
                payload["timestamp"] = datetime.now().isoformat()
            
            # Add topic
            payload["topic"] = msg.topic
            
            # Call all registered callbacks
            for callback in self.callbacks:
                callback(payload)
            
        except json.JSONDecodeError:
            print(f"Failed to decode MQTT message: {msg.payload}")
        except Exception as e:
            print(f"Error processing MQTT message: {e}")
    
    def _on_disconnect(self, client, userdata, rc):
        """
        MQTT disconnection callback
        """
        print(f"MQTT disconnected with code: {rc}")
        self.is_connected = False
    
    @staticmethod
    def process_device_reading(
        db: Session,
        reading_data: Dict[str, Any]
    ) -> Optional[IoTReading]:
        """
        Process and store IoT device reading
        """
        try:
            # Extract device ID from topic or data
            device_id = reading_data.get("device_id")
            if not device_id:
                # Try to extract from topic
                topic = reading_data.get("topic", "")
                parts = topic.split("/")
                if len(parts) >= 3:
                    device_id = parts[2]
            
            if not device_id:
                print("No device ID in reading data")
                return None
            
            # Get device from database
            device = db.query(IoTDevice).filter(
                IoTDevice.device_id == device_id
            ).first()
            
            if not device:
                print(f"Device not found: {device_id}")
                return None
            
            # Create reading record
            reading = IoTReading(
                device_id=device.id,
                reading_type=reading_data.get("reading_type", "unknown"),
                value=reading_data.get("value", 0),
                unit=reading_data.get("unit", "unknown"),
                timestamp=datetime.fromisoformat(reading_data.get("timestamp")),
                latitude=reading_data.get("latitude"),
                longitude=reading_data.get("longitude"),
            )
            
            db.add(reading)
            db.commit()
            db.refresh(reading)
            
            print(f"Stored reading from device {device_id}: {reading_data}")
            return reading
            
        except Exception as e:
            print(f"Failed to process device reading: {e}")
            db.rollback()
            return None
    
    @staticmethod
    def simulate_device_readings(
        db: Session,
        campus_id: int,
        count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Simulate IoT device readings for testing
        """
        readings = []
        
        # Get buildings for this campus
        from backend.models.campus import Building
        buildings = db.query(Building).filter(Building.campus_id == campus_id).all()
        
        if not buildings:
            return readings
        
        # Device types and their typical values
        device_types = {
            "energy_meter": {
                "reading_type": "energy_kwh",
                "unit": "kWh",
                "min_value": 0.1,
                "max_value": 10.0,
            },
            "water_meter": {
                "reading_type": "water_liters",
                "unit": "liters",
                "min_value": 100,
                "max_value": 1000,
            },
            "temperature_sensor": {
                "reading_type": "temperature_c",
                "unit": "°C",
                "min_value": 15,
                "max_value": 35,
            },
            "humidity_sensor": {
                "reading_type": "humidity",
                "unit": "%",
                "min_value": 30,
                "max_value": 80,
            },
            "waste_sensor": {
                "reading_type": "waste_kg",
                "unit": "kg",
                "min_value": 0,
                "max_value": 50,
            },
        }
        
        import random
        
        for i in range(count):
            # Select random building
            building = random.choice(buildings)
            
            # Select random device type
            device_type, device_spec = random.choice(list(device_types.items()))
            
            # Generate reading
            reading_data = {
                "device_id": f"SIM_{building.id}_{device_type}_{i}",
                "building_id": building.id,
                "building_name": building.name,
                "reading_type": device_spec["reading_type"],
                "value": round(random.uniform(
                    device_spec["min_value"],
                    device_spec["max_value"]
                ), 2),
                "unit": device_spec["unit"],
                "timestamp": datetime.now().isoformat(),
                "latitude": 26.9124 + random.uniform(-0.001, 0.001),  # LNMIIT coordinates
                "longitude": 75.7873 + random.uniform(-0.001, 0.001),
                "is_simulated": True,
            }
            
            readings.append(reading_data)
            
            # Also store in database if requested
            IoTService.process_device_reading(db, reading_data)
        
        return readings


# Global IoT service instance
iot_service = IoTService()


def start_iot_service():
    """
    Start the IoT service
    """
    iot_service.connect()
    return iot_service


def stop_iot_service():
    """
    Stop the IoT service
    """
    iot_service.disconnect()