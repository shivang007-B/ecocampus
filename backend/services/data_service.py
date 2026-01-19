"""
Data Service for handling campus data operations
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from backend.utils.helpers import generate_mock_campus_data, get_real_weather_data
from backend.services.carbon_calculator import CarbonCalculator
from backend.models.campus import Campus, Building, Department
from backend.models.carbon import CampusEmission, EmissionTarget
from backend.schemas.carbon import EmissionCreate, EmissionUpdate


class DataService:
    """
    Service for handling campus data operations
    """
    
    @staticmethod
    def generate_mock_emissions(
        db: Session,
        campus_id: int,
        days: int = 30
    ) -> List[CampusEmission]:
        """
        Generate mock emission data for a campus
        """
        mock_data = generate_mock_campus_data(days)
        emissions = []
        
        for day_data in mock_data:
            # Calculate emissions
            calculation = CarbonCalculator.calculate_total_campus_emission(
                electricity_kwh=day_data["electricity_kwh"],
                transport_data=day_data["transport"],
                waste_data={"mixed": day_data["waste_kg"]},
                meals_data=day_data["meals"],
                water_liters=day_data.get("water_liters", 0)
            )
            
            # Create emission record
            emission = CampusEmission(
                campus_id=campus_id,
                date=datetime.strptime(day_data["date"], "%Y-%m-%d"),
                electricity_emission=calculation["breakdown"]["electricity_kg"],
                transportation_emission=calculation["breakdown"]["transport_kg"],
                waste_emission=calculation["breakdown"]["waste_kg"],
                food_emission=calculation["breakdown"]["food_kg"],
                water_emission=calculation["breakdown"]["water_kg"],
                total_emission=calculation["total_emission_kg"],
                temperature=day_data.get("temperature"),
                humidity=day_data.get("humidity"),
                data_source="simulated"
            )
            
            emissions.append(emission)
        
        return emissions
    
    @staticmethod
    def get_campus_summary(db: Session, campus_id: int) -> Dict[str, Any]:
        """
        Get comprehensive campus summary
        """
        campus = db.query(Campus).filter(Campus.id == campus_id).first()
        if not campus:
            return {}
        
        # Get today's date
        today = datetime.now().date()
        
        # Get emissions for today
        today_emission = db.query(CampusEmission).filter(
            CampusEmission.campus_id == campus_id,
            CampusEmission.date >= today,
            CampusEmission.date < today + timedelta(days=1)
        ).first()
        
        # Get emissions for this week
        week_start = today - timedelta(days=today.weekday())
        week_emissions = db.query(CampusEmission).filter(
            CampusEmission.campus_id == campus_id,
            CampusEmission.date >= week_start
        ).all()
        
        # Get emissions for this month
        month_start = today.replace(day=1)
        month_emissions = db.query(CampusEmission).filter(
            CampusEmission.campus_id == campus_id,
            CampusEmission.date >= month_start
        ).all()
        
        # Calculate totals
        total_week = sum(e.total_emission for e in week_emissions)
        total_month = sum(e.total_emission for e in month_emissions)
        
        # Get active targets
        active_targets = db.query(EmissionTarget).filter(
            EmissionTarget.campus_id == campus_id,
            EmissionTarget.is_active == True
        ).all()
        
        # Get buildings and departments
        buildings = db.query(Building).filter(Building.campus_id == campus_id).all()
        departments = db.query(Department).filter(Department.campus_id == campus_id).all()
        
        # Calculate targets progress
        target_progress = 0
        if active_targets and total_month > 0:
            # For simplicity, take the first active target
            target = active_targets[0]
            progress = (target.baseline_value - total_month) / target.baseline_value * 100
            target_progress = max(0, min(100, progress))
        
        summary = {
            "campus_name": campus.name,
            "campus_id": campus.id,
            "student_count": campus.student_count,
            "staff_count": campus.staff_count,
            "area_sqm": campus.area_sqm,
            "building_count": campus.building_count,
            "today_emission": today_emission.total_emission if today_emission else 0,
            "week_emission": total_week,
            "month_emission": total_month,
            "target_progress": target_progress,
            "active_targets": len(active_targets),
            "building_count": len(buildings),
            "department_count": len(departments),
            "last_updated": datetime.now().isoformat()
        }
        
        return summary
    
    @staticmethod
    def get_emission_trends(
        db: Session,
        campus_id: int,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get emission trends for the last N days
        """
        start_date = datetime.now() - timedelta(days=days)
        
        emissions = db.query(CampusEmission).filter(
            CampusEmission.campus_id == campus_id,
            CampusEmission.date >= start_date
        ).order_by(CampusEmission.date).all()
        
        trends = []
        for emission in emissions:
            trends.append({
                "date": emission.date.strftime("%Y-%m-%d"),
                "total": emission.total_emission,
                "electricity": emission.electricity_emission,
                "transport": emission.transportation_emission,
                "waste": emission.waste_emission,
                "food": emission.food_emission,
                "water": emission.water_emission,
                "temperature": emission.temperature,
                "humidity": emission.humidity,
            })
        
        return trends
    
    @staticmethod
    def get_emission_breakdown(
        db: Session,
        campus_id: int,
        period: str = "month"
    ) -> Dict[str, float]:
        """
        Get emission breakdown by source for a period
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
        ).all()
        
        if not emissions:
            return {
                "electricity": 0,
                "transport": 0,
                "waste": 0,
                "food": 0,
                "water": 0,
                "other": 0,
                "total": 0
            }
        
        # Sum up emissions by source
        breakdown = {
            "electricity": sum(e.electricity_emission for e in emissions),
            "transport": sum(e.transportation_emission for e in emissions),
            "waste": sum(e.waste_emission for e in emissions),
            "food": sum(e.food_emission for e in emissions),
            "water": sum(e.water_emission for e in emissions),
            "other": sum(e.other_emission for e in emissions),
        }
        
        total = sum(breakdown.values())
        
        # Calculate percentages
        percentages = {}
        for source, value in breakdown.items():
            percentages[source] = (value / total * 100) if total > 0 else 0
        
        breakdown["total"] = total
        breakdown["percentages"] = percentages
        
        return breakdown
    
    @staticmethod
    def get_leaderboard_data(
        db: Session,
        campus_id: int,
        period: str = "week"
    ) -> Dict[str, Any]:
        """
        Get leaderboard data for departments and buildings
        """
        # For now, return mock leaderboard data
        # In production, this would calculate actual savings
        
        departments = db.query(Department).filter(
            Department.campus_id == campus_id
        ).all()
        
        buildings = db.query(Building).filter(
            Building.campus_id == campus_id
        ).all()
        
        # Generate mock savings data
        department_leaderboard = []
        for dept in departments:
            savings = random.uniform(50, 500)  # Mock savings in kg
            department_leaderboard.append({
                "name": dept.name,
                "code": dept.code,
                "carbon_saved_kg": round(savings, 2),
                "student_count": dept.student_count,
                "savings_per_student": round(savings / max(dept.student_count, 1), 2)
            })
        
        building_leaderboard = []
        for building in buildings:
            savings = random.uniform(100, 1000)  # Mock savings in kg
            building_leaderboard.append({
                "name": building.name,
                "type": building.building_type,
                "carbon_saved_kg": round(savings, 2),
                "area_sqm": building.area_sqm,
                "savings_per_area": round(savings / max(building.area_sqm, 1), 2)
            })
        
        # Sort by savings
        department_leaderboard.sort(key=lambda x: x["carbon_saved_kg"], reverse=True)
        building_leaderboard.sort(key=lambda x: x["carbon_saved_kg"], reverse=True)
        
        total_participants = len(departments) + len(buildings)
        total_savings = sum(d["carbon_saved_kg"] for d in department_leaderboard) + \
                       sum(b["carbon_saved_kg"] for b in building_leaderboard)
        
        return {
            "period": period,
            "total_participants": total_participants,
            "total_carbon_saved_kg": round(total_savings, 2),
            "average_savings_kg": round(total_savings / max(total_participants, 1), 2),
            "top_departments": department_leaderboard[:5],
            "top_buildings": building_leaderboard[:5],
            "last_updated": datetime.now().isoformat()
        }
    
    @staticmethod
    def calculate_savings_scenario(
        db: Session,
        campus_id: int,
        scenario: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate potential savings for a scenario
        """
        # Get baseline emissions
        baseline = db.query(CampusEmission).filter(
            CampusEmission.campus_id == campus_id
        ).order_by(CampusEmission.date.desc()).first()
        
        if not baseline:
            baseline_emission = 100000  # Default baseline if no data
        else:
            # Convert daily to annual (approximate)
            baseline_emission = baseline.total_emission * 365
        
        # Calculate savings
        calculator = CarbonCalculator()
        result = calculator.calculate_emission_reduction_scenario(
            baseline_emission,
            scenario
        )
        
        # Add cost estimations
        cost_breakdown = {}
        total_cost = 0
        
        if "solar_panels_kw" in scenario:
            solar_cost = scenario["solar_panels_kw"] * 50000  # ~₹50,000 per kW
            cost_breakdown["solar_panels"] = solar_cost
            total_cost += solar_cost
        
        if "led_bulbs_count" in scenario:
            led_cost = scenario["led_bulbs_count"] * 200  # ~₹200 per bulb
            cost_breakdown["led_lighting"] = led_cost
            total_cost += led_cost
        
        if "electric_vehicles_count" in scenario:
            ev_cost = scenario["electric_vehicles_count"] * 1000000  # ~₹10 lakh per vehicle
            cost_breakdown["electric_vehicles"] = ev_cost
            total_cost += ev_cost
        
        if "tree_planting_count" in scenario:
            tree_cost = scenario["tree_planting_count"] * 500  # ~₹500 per tree
            cost_breakdown["tree_planting"] = tree_cost
            total_cost += tree_cost
        
        # Calculate payback period
        annual_savings = result["total_reduction_kg"]
        # Assuming carbon credit price of ₹500 per ton (1000 kg)
        annual_monetary_savings = (annual_savings / 1000) * 500
        
        payback_years = total_cost / annual_monetary_savings if annual_monetary_savings > 0 else 0
        
        result["cost_breakdown"] = cost_breakdown
        result["total_cost"] = total_cost
        result["annual_monetary_savings"] = annual_monetary_savings
        result["payback_years"] = payback_years
        
        return result
    
    @staticmethod
    def update_real_time_data(
        db: Session,
        campus_id: int
    ) -> Dict[str, Any]:
        """
        Update campus with real-time data (weather, etc.)
        """
        # Get real weather data
        weather = get_real_weather_data("Jaipur")
        
        # Get or create today's emission record
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        emission = db.query(CampusEmission).filter(
            CampusEmission.campus_id == campus_id,
            CampusEmission.date >= today,
            CampusEmission.date < today + timedelta(days=1)
        ).first()
        
        if not emission:
            # Create new record for today
            emission = CampusEmission(
                campus_id=campus_id,
                date=datetime.now(),
                temperature=weather["temperature"],
                humidity=weather["humidity"],
                data_source="real_time"
            )
            db.add(emission)
        else:
            # Update existing record
            emission.temperature = weather["temperature"]
            emission.humidity = weather["humidity"]
            emission.data_source = "real_time"
        
        db.commit()
        db.refresh(emission)
        
        return {
            "status": "updated",
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "timestamp": datetime.now().isoformat()
        }