"""
Carbon Calculator Service
Calculates carbon emissions from various campus activities
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import math
from backend.utils.constants import (
    ELECTRICITY_EMISSION_FACTOR,
    TRANSPORT_EMISSION_FACTORS,
    WASTE_EMISSION_FACTORS,
    FOOD_EMISSION_FACTORS,
    BUILDING_EMISSION_FACTORS,
)


class CarbonCalculator:
    """
    Main carbon calculator class
    """
    
    @staticmethod
    def calculate_electricity_emission(kwh: float, grid_factor: Optional[float] = None) -> float:
        """
        Calculate CO2 emissions from electricity consumption
        
        Args:
            kwh: Electricity consumption in kWh
            grid_factor: Emission factor for electricity grid (kgCO2e/kWh)
                        If None, uses default Indian grid factor
        
        Returns:
            CO2 emissions in kg
        """
        factor = grid_factor if grid_factor is not None else ELECTRICITY_EMISSION_FACTOR
        return kwh * factor
    
    @staticmethod
    def calculate_transport_emission(
        transport_data: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Calculate CO2 emissions from transportation
        
        Args:
            transport_data: Dictionary with transport modes and distances
                          Example: {"petrol_car": 100, "diesel_bus": 50}
        
        Returns:
            Dictionary with total emissions and breakdown
        """
        total_emission = 0.0
        breakdown = {}
        
        for transport_mode, distance_km in transport_data.items():
            if transport_mode in TRANSPORT_EMISSION_FACTORS:
                emission = distance_km * TRANSPORT_EMISSION_FACTORS[transport_mode]
                total_emission += emission
                breakdown[transport_mode] = {
                    "distance_km": distance_km,
                    "emission_kg": emission
                }
        
        return {
            "total_emission_kg": total_emission,
            "breakdown": breakdown,
            "transport_modes_used": list(transport_data.keys())
        }
    
    @staticmethod
    def calculate_waste_emission(
        waste_data: Dict[str, float],
        treatment_method: str = "landfill"
    ) -> Dict[str, Any]:
        """
        Calculate CO2 emissions from waste
        
        Args:
            waste_data: Dictionary with waste types and amounts in kg
                      Example: {"organic": 100, "plastic": 50, "paper": 30}
            treatment_method: Waste treatment method
        
        Returns:
            Dictionary with total emissions and breakdown
        """
        total_emission = 0.0
        breakdown = {}
        
        if treatment_method in WASTE_EMISSION_FACTORS:
            factor = WASTE_EMISSION_FACTORS[treatment_method]
            
            for waste_type, amount_kg in waste_data.items():
                emission = amount_kg * factor
                total_emission += emission
                breakdown[waste_type] = {
                    "amount_kg": amount_kg,
                    "emission_kg": emission
                }
        
        return {
            "total_emission_kg": total_emission,
            "breakdown": breakdown,
            "treatment_method": treatment_method
        }
    
    @staticmethod
    def calculate_food_emission(meals_data: Dict[str, int]) -> Dict[str, Any]:
        """
        Calculate CO2 emissions from food consumption
        
        Args:
            meals_data: Dictionary with meal types and counts
                      Example: {"beef": 10, "vegetarian": 50, "vegan": 20}
        
        Returns:
            Dictionary with total emissions and breakdown
        """
        total_emission = 0.0
        breakdown = {}
        
        for meal_type, meal_count in meals_data.items():
            if meal_type in FOOD_EMISSION_FACTORS:
                emission = meal_count * FOOD_EMISSION_FACTORS[meal_type]
                total_emission += emission
                breakdown[meal_type] = {
                    "meal_count": meal_count,
                    "emission_kg": emission
                }
        
        return {
            "total_emission_kg": total_emission,
            "breakdown": breakdown,
            "total_meals": sum(meals_data.values())
        }
    
    @staticmethod
    def calculate_building_emission(
        building_type: str,
        area_sqm: float,
        occupancy_rate: float = 0.8,
        heating_cooling_factor: float = 1.0
    ) -> float:
        """
        Calculate baseline CO2 emissions for a building
        
        Args:
            building_type: Type of building (hostel, academic, etc.)
            area_sqm: Building area in square meters
            occupancy_rate: Occupancy rate (0.0 to 1.0)
            heating_cooling_factor: Factor for heating/cooling needs
        
        Returns:
            Annual CO2 emissions in kg
        """
        if building_type in BUILDING_EMISSION_FACTORS:
            base_emission = BUILDING_EMISSION_FACTORS[building_type]
            annual_emission = base_emission * area_sqm * occupancy_rate * heating_cooling_factor
            return annual_emission
        return 0.0
    
    @staticmethod
    def calculate_water_emission(water_liters: float) -> float:
        """
        Calculate CO2 emissions from water consumption
        
        Args:
            water_liters: Water consumption in liters
        
        Returns:
            CO2 emissions in kg
        """
        # Emission factor for water treatment and distribution
        # Source: Average from water utility reports
        WATER_EMISSION_FACTOR = 0.00034  # kgCO2e per liter
        return water_liters * WATER_EMISSION_FACTOR
    
    @staticmethod
    def calculate_total_campus_emission(
        electricity_kwh: float,
        transport_data: Dict[str, float],
        waste_data: Dict[str, float],
        meals_data: Dict[str, int],
        water_liters: float = 0,
        other_emission: float = 0
    ) -> Dict[str, Any]:
        """
        Calculate total campus emissions from all sources
        
        Returns comprehensive emission report
        """
        # Calculate each component
        electricity = CarbonCalculator.calculate_electricity_emission(electricity_kwh)
        transport = CarbonCalculator.calculate_transport_emission(transport_data)
        waste = CarbonCalculator.calculate_waste_emission(waste_data)
        food = CarbonCalculator.calculate_food_emission(meals_data)
        water = CarbonCalculator.calculate_water_emission(water_liters)
        
        total = electricity + transport["total_emission_kg"] + \
                waste["total_emission_kg"] + food["total_emission_kg"] + \
                water + other_emission
        
        # Calculate percentages
        percentages = {
            "electricity": (electricity / total * 100) if total > 0 else 0,
            "transport": (transport["total_emission_kg"] / total * 100) if total > 0 else 0,
            "waste": (waste["total_emission_kg"] / total * 100) if total > 0 else 0,
            "food": (food["total_emission_kg"] / total * 100) if total > 0 else 0,
            "water": (water / total * 100) if total > 0 else 0,
            "other": (other_emission / total * 100) if total > 0 else 0,
        }
        
        return {
            "total_emission_kg": total,
            "breakdown": {
                "electricity_kg": electricity,
                "transport_kg": transport["total_emission_kg"],
                "waste_kg": waste["total_emission_kg"],
                "food_kg": food["total_emission_kg"],
                "water_kg": water,
                "other_kg": other_emission,
            },
            "percentages": percentages,
            "details": {
                "transport": transport,
                "waste": waste,
                "food": food,
            }
        }
    
    @staticmethod
    def calculate_emission_reduction_scenario(
        baseline_emission: float,
        reduction_measures: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate potential emission reductions from various measures
        
        Args:
            baseline_emission: Baseline annual emissions in kg
            reduction_measures: Dictionary with reduction measures
        
        Returns:
            Dictionary with reduction calculations
        """
        reductions = {}
        total_reduction = 0.0
        
        # Solar panels (kW to kWh conversion)
        if "solar_panels_kw" in reduction_measures:
            solar_kw = reduction_measures["solar_panels_kw"]
            # Assuming 4.5 hours of effective sunlight per day in India
            annual_generation = solar_kw * 4.5 * 365
            reduction = annual_generation * ELECTRICITY_EMISSION_FACTOR
            reductions["solar_panels"] = reduction
            total_reduction += reduction
        
        # LED lighting
        if "led_bulbs_count" in reduction_measures:
            led_count = reduction_measures["led_bulbs_count"]
            # Assuming 0.05 kWh saving per bulb per day
            annual_saving = led_count * 0.05 * 365
            reduction = annual_saving * ELECTRICITY_EMISSION_FACTOR
            reductions["led_lighting"] = reduction
            total_reduction += reduction
        
        # Electric vehicles
        if "electric_vehicles_count" in reduction_measures:
            ev_count = reduction_measures["electric_vehicles_count"]
            # Assuming 1500 km per vehicle per year
            km_per_year = ev_count * 1500
            # Difference between petrol and electric
            petrol_emission = km_per_year * TRANSPORT_EMISSION_FACTORS["petrol_car"]
            electric_emission = km_per_year * TRANSPORT_EMISSION_FACTORS["electric_car"]
            reduction = petrol_emission - electric_emission
            reductions["electric_vehicles"] = reduction
            total_reduction += reduction
        
        # Waste reduction
        if "waste_reduction_percent" in reduction_measures:
            waste_reduction = reduction_measures["waste_reduction_percent"] / 100
            # Assuming baseline waste emission
            baseline_waste = baseline_emission * 0.1  # Assuming 10% from waste
            reduction = baseline_waste * waste_reduction
            reductions["waste_reduction"] = reduction
            total_reduction += reduction
        
        # Diet change
        if "meat_reduction_percent" in reduction_measures:
            diet_reduction = reduction_measures["meat_reduction_percent"] / 100
            # Assuming baseline food emission
            baseline_food = baseline_emission * 0.15  # Assuming 15% from food
            reduction = baseline_food * diet_reduction
            reductions["diet_change"] = reduction
            total_reduction += reduction
        
        # Tree planting
        if "tree_planting_count" in reduction_measures:
            tree_count = reduction_measures["tree_planting_count"]
            # Assuming 21.77 kg CO2 absorbed per tree per year
            reduction = tree_count * 21.77
            reductions["tree_planting"] = reduction
            total_reduction += reduction
        
        new_total = baseline_emission - total_reduction
        reduction_percentage = (total_reduction / baseline_emission * 100) if baseline_emission > 0 else 0
        
        return {
            "baseline_emission_kg": baseline_emission,
            "total_reduction_kg": total_reduction,
            "new_total_emission_kg": new_total,
            "reduction_percentage": reduction_percentage,
            "reduction_breakdown": reductions,
            "equivalent_trees": total_reduction / 21.77,  # Trees needed to absorb this reduction
            "equivalent_cars": total_reduction / 4600,  # Average car emissions per year
        }
    
    @staticmethod
    def calculate_emission_intensity(
        total_emission: float,
        student_count: int,
        area_sqm: float
    ) -> Dict[str, float]:
        """
        Calculate emission intensity metrics
        
        Returns:
            Dictionary with intensity metrics
        """
        metrics = {}
        
        if student_count > 0:
            metrics["emission_per_student"] = total_emission / student_count
        
        if area_sqm > 0:
            metrics["emission_per_area"] = total_emission / area_sqm
        
        return metrics