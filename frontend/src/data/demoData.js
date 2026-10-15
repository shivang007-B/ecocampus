// ─── EcoCampus Demo Data ────────────────────────────────────────────────────
// Used as fallback when backend is unavailable (e.g. hackathon demo mode)

export const DEMO_STATS = {
  totalEmissions: 185499,
  monthlyTarget: 222599,
  electricityEmissions: 112340,
  transportationEmissions: 38420,
  wasteEmissions: 14230,
  waterEmissions: 9870,
  foodEmissions: 10639,
}

export const DEMO_CHART_DATA = [
  { name: 'Electricity', value: 112340 },
  { name: 'Transport',   value: 38420  },
  { name: 'Food',        value: 10639  },
  { name: 'Waste',       value: 14230  },
  { name: 'Water',       value: 9870   },
]

// 30 days of realistic declining trend
export const DEMO_TREND_DATA = (() => {
  const days = 30
  const base = new Date('2026-09-17')
  return Array.from({ length: days }, (_, i) => {
    const d = new Date(base)
    d.setDate(base.getDate() + i)
    const noise = Math.sin(i * 0.7) * 1200 + Math.random() * 800
    const trend = 7200 - i * 40
    return {
      date: d.toISOString().slice(0, 10),
      emissions: Math.round(Math.max(5000, trend + noise)),
    }
  })
})()

export const DEMO_IOT_DEVICES = [
  { id: 'SMART_METER_01',  name: 'Academic Block Energy Meter',  value: '247 kWh', glow: 'text-emerald-400' },
  { id: 'WATER_SENSOR_01', name: 'Hostel Water Flow Sensor',     value: '1,840 L', glow: 'text-cyan-400'   },
  { id: 'AQI_MONITOR_01',  name: 'Library Air Quality Sensor',   value: '43 AQI',  glow: 'text-emerald-400'},
  { id: 'WASTE_SENSOR_01', name: 'Cafeteria Waste Bin Sensor',   value: '12.4 kg', glow: 'text-amber-400'  },
]

export const DEMO_EMISSIONS_LOG = Array.from({ length: 30 }, (_, i) => {
  const d = new Date('2026-10-15')
  d.setDate(d.getDate() - i)
  const elec  = 5000 + Math.round(Math.random() * 4000)
  const trans = 3800 + Math.round(Math.random() * 1800)
  const waste = 200  + Math.round(Math.random() * 300)
  const water = 200  + Math.round(Math.random() * 200)
  const food  = 900  + Math.round(Math.random() * 600)
  return {
    id: i + 1,
    campus_id: 1,
    electricity_emission: elec,
    transportation_emission: trans,
    waste_emission: waste,
    water_emission: water,
    food_emission: food,
    total_emission: elec + trans + waste + water + food,
    date: d.toISOString(),
    notes: [
      'Automated campus IoT batch',
      'Peak weekday consumption',
      'Green Energy Switch Day',
      'Solar offset applied',
      'EV Fleet charge cycle',
      'Low-occupancy weekend batch',
    ][i % 6],
  }
})

export const DEMO_CAMPUSES = [
  {
    id: 1,
    name: 'EcoCampus Demo',
    location: 'Green Park, Smart City',
    area_sqm: 100000,
    student_count: 5000,
    staff_count: 500,
    building_count: 7,
  },
]

export const DEMO_BUILDINGS = [
  { id: 1, name: 'Main Academic Block',     type: 'Academic',      area: '20,000 sqm', energy: 'Rating A+', floors: 5 },
  { id: 2, name: 'Computer Science Dept',   type: 'Lab & Research', area: '5,000 sqm',  energy: 'Rating A',  floors: 4 },
  { id: 3, name: 'Boys Hostel Complex A',   type: 'Residential',   area: '15,000 sqm', energy: 'Rating B',  floors: 4 },
  { id: 4, name: 'Girls Hostel Complex B',  type: 'Residential',   area: '12,000 sqm', energy: 'Rating A',  floors: 4 },
  { id: 5, name: 'Central Digital Library', type: 'Academic',      area: '8,000 sqm',  energy: 'Rating A+', floors: 3 },
  { id: 6, name: 'Eco Dining & Cafeteria',  type: 'Cafeteria',     area: '3,000 sqm',  energy: 'Rating B',  floors: 2 },
  { id: 7, name: 'Computer Lab Block',      type: 'Lab & Research', area: '4,000 sqm',  energy: 'Rating A',  floors: 3 },
]
