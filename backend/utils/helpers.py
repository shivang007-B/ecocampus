import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
import requests
from backend.core.config import settings


def generate_mock_campus_data(days: int = 30) -> List[Dict[str, Any]]:
    """
    Generate realistic mock data for campus emissions
    """
    data = []
    base_date = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        current_date = base_date + timedelta(days=day)
        
        # Weekday/weekend variation
        is_weekend = current_date.weekday() >= 5
        
        # Seasonal variation (simulate higher AC use in summer)
        month = current_date.month
        seasonal_factor = 1.0
        if month in [5, 6, 7, 8]:  # Summer months
            seasonal_factor = 1.3
        elif month in [11, 12, 1]:  # Winter months
            seasonal_factor = 0.8
        
        # Weekend reduction
        day_factor = 0.7 if is_weekend else 1.0
        
        # Random but realistic data
        daily_data = {
            "date": current_date.strftime("%Y-%m-%d"),
            "electricity_kwh": random.randint(8000, 12000) * seasonal_factor * day_factor,
            "water_liters": random.randint(200000, 300000) * day_factor,
            "waste_kg": random.randint(800, 1200) * day_factor,
            "transport": {
                "cars": random.randint(800, 1200) * day_factor,
                "bikes": random.randint(400, 600) * day_factor,
                "buses": random.randint(20, 40),
                "walking": random.randint(1000, 1500) * day_factor,
                "cycling": random.randint(200, 400) * day_factor,
            },
            "meals": {
                "beef": random.randint(100, 300) * day_factor,
                "chicken": random.randint(500, 800) * day_factor,
                "vegetarian": random.randint(2000, 3000) * day_factor,
                "vegan": random.randint(300, 600) * day_factor,
            },
            "temperature": random.uniform(15, 35),  # Jaipur temperature range
            "humidity": random.uniform(30, 80),
        }
        
        data.append(daily_data)
    
    return data


def get_real_weather_data(city: str = "Jaipur") -> Dict[str, Any]:
    """
    Fetch real weather data from OpenWeatherMap API
    """
    if not settings.OPENWEATHER_API_KEY:
        return {"temperature": 25, "humidity": 50}
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        if response.status_code == 200:
            return {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["main"],
                "wind_speed": data["wind"]["speed"],
            }
    except Exception:
        pass
    
    # Fallback to mock data
    return {"temperature": 25, "humidity": 50}


def calculate_carbon_savings(scenario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate potential carbon savings for a scenario
    """
    savings = {
        "solar_panels": scenario.get("solar_kw", 0) * 4 * 365,  # 4 kWh per kW per day
        "led_lights": scenario.get("led_count", 0) * 0.05 * 365,  # 0.05 kWh saved per bulb per day
        "electric_vehicles": scenario.get("ev_count", 0) * 1500,  # 1500 km per year, 0.15 kg/km saved
        "waste_reduction": scenario.get("waste_reduction_percent", 0) * 1000,  # 1000 kg base waste
        "meat_reduction": scenario.get("meat_reduction_percent", 0) * 10000,  # 10000 meals base
    }
    
    total_savings = sum(savings.values())
    
    return {
        "savings_breakdown": savings,
        "total_savings_kg": total_savings,
        "equivalent_trees": total_savings / 21.77,  # One tree absorbs ~21.77 kg CO2 per year
        "equivalent_cars": total_savings / 4600,  # Average car emits ~4600 kg CO2 per year
    }


def format_emission_value(value: float) -> str:
    """
    Format emission values for display
    """
    if value >= 1000000:  # Million
        return f"{value/1000000:.2f}M kg"
    elif value >= 1000:  # Thousand
        return f"{value/1000:.2f}k kg"
    else:
        return f"{value:.2f} kg"