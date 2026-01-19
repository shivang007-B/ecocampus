"""
Emission factors for India (kgCO2e per unit)
Source: IPCC 2023, Indian government reports
"""

# Electricity emission factor (kgCO2e per kWh)
# Average for Indian grid
ELECTRICITY_EMISSION_FACTOR = 0.82

# Transportation emission factors (kgCO2e per km)
TRANSPORT_EMISSION_FACTORS = {
    "petrol_car": 0.192,
    "diesel_car": 0.171,
    "cng_car": 0.145,
    "electric_car": 0.05,  # Assuming renewable energy
    "petrol_bike": 0.103,
    "diesel_bus": 0.089,
    "electric_bus": 0.02,
    "walking": 0.0,
    "cycling": 0.0,
}

# Waste emission factors (kgCO2e per kg)
WASTE_EMISSION_FACTORS = {
    "landfill": 0.1,
    "compost": 0.02,
    "recycled": 0.05,
    "incinerated": 0.3,
}

# Food emission factors (kgCO2e per meal)
FOOD_EMISSION_FACTORS = {
    "beef": 6.0,
    "lamb": 5.0,
    "pork": 3.0,
    "chicken": 2.0,
    "fish": 3.0,
    "vegetarian": 1.0,
    "vegan": 0.5,
}

# Building types and base emissions (kgCO2e per sqm per year)
BUILDING_EMISSION_FACTORS = {
    "hostel": 120,
    "academic": 150,
    "library": 140,
    "cafeteria": 200,
    "lab": 180,
    "office": 130,
}

# Campus areas in square meters (example for LNMIIT)
CAMPUS_AREAS = {
    "main_campus": 100000,
    "hostel_complex": 50000,
    "academic_block": 30000,
    "sports_complex": 20000,
}