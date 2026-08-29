import React, { useState, useEffect } from 'react'
import { TrendingDown, Target, Zap, Droplets, Trash2, Cpu, Activity, ArrowDownRight, RefreshCw } from 'lucide-react'
import { EmissionChart, TrendChart, BreakdownChart } from '../components/Charts'
import { carbonAPI, iotAPI } from '../api/client'
import toast from 'react-hot-toast'
import EcoCard from '../components/EcoCard'
import EcoButton from '../components/EcoButton'

export default function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalEmissions: 14100,
    monthlyTarget: 18000,
    electricityEmissions: 5234,
    transportationEmissions: 4890,
    wasteEmissions: 2326,
    waterEmissions: 450,
    foodEmissions: 1200,
  })
  const [chartData, setChartData] = useState([])
  const [trendData, setTrendData] = useState([])
  const [iotStatus, setIotStatus] = useState([])

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      
      const [emissionsRes, trendsRes, iotRes] = await Promise.allSettled([
        carbonAPI.getEmissions(),
        carbonAPI.getTrends(),
        iotAPI.getDevices()
      ])

      // Populate Chart Data
      setChartData([
        { name: 'Electricity', value: 5234 },
        { name: 'Transport', value: 4890 },
        { name: 'Waste', value: 2326 },
        { name: 'Food', value: 1200 },
        { name: 'Water', value: 450 },
      ])

      setTrendData([
        { date: 'Aug 01', emissions: 15400 },
        { date: 'Aug 08', emissions: 14900 },
        { date: 'Aug 15', emissions: 14600 },
        { date: 'Aug 22', emissions: 14350 },
        { date: 'Aug 29', emissions: 14100 },
      ])

      setIotStatus([
        { id: 'SMART_METER_01', name: 'Main Academic Energy Meter', type: 'energy_meter', value: '412 kWh', status: 'active', glow: 'text-emerald-400' },
        { id: 'WATER_SENSOR_01', name: 'Hostel A Water Flow Telemetry', type: 'water_meter', value: '1,240 L', status: 'active', glow: 'text-cyan-400' },
        { id: 'AQI_MONITOR_01', name: 'Library Clean Air Monitor', type: 'temperature_sensor', value: '38 AQI', status: 'active', glow: 'text-emerald-400' },
        { id: 'WASTE_SENSOR_01', name: 'Cafeteria Recycling Sensor', type: 'waste_sensor', value: '185 kg', status: 'active', glow: 'text-amber-400' },
      ])
    } catch (error) {
      toast.error('Failed to update telemetry feeds')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-96 gap-4 font-mono">
        <div className="w-12 h-12 rounded-full border-2 border-emerald-500 border-t-transparent animate-spin" />
        <p className="text-xs text-[#10F0A0] uppercase tracking-widest animate-pulse">Initializing Cyber Telemetry Dashboard...</p>
      </div>
    )
  }

  const completionPercent = Math.min(100, (stats.totalEmissions / stats.monthlyTarget) * 100)
  const remainingBudget = stats.monthlyTarget - stats.totalEmissions

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-white flex items-center gap-2">
            Campus GHG Telemetry <span className="text-[#10F0A0] text-sm font-mono font-normal">● LIVE</span>
          </h1>
          <p className="text-xs font-mono text-gray-400 mt-1">Real-time Scope 1, 2 & 3 emissions analytics for EcoCampus Demo</p>
        </div>
        <div className="flex items-center gap-3">
          <EcoButton variant="outline" onClick={fetchDashboardData} className="text-xs py-2">
            <RefreshCw className="w-3.5 h-3.5 inline" /> Sync Telemetry
          </EcoButton>
        </div>
      </div>

      {/* Top Stat Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <EcoCard
          title="Net Carbon Footprint"
          value={stats.totalEmissions.toLocaleString()}
          subtitle="kg CO₂e"
          icon={TrendingDown}
          trend="-8.4%"
        />
        <EcoCard
          title="Electricity Emissions"
          value={stats.electricityEmissions.toLocaleString()}
          subtitle="kg CO₂"
          icon={Zap}
        />
        <EcoCard
          title="Transport Emissions"
          value={stats.transportationEmissions.toLocaleString()}
          subtitle="kg CO₂"
          icon={Activity}
        />
        <EcoCard
          title="Reduction Target"
          value={`${completionPercent.toFixed(1)}%`}
          subtitle={`Budget: ${stats.monthlyTarget.toLocaleString()} kg`}
          icon={Target}
        >
          <div className="w-full bg-[#080c0e] h-2 rounded-full overflow-hidden border border-emerald-500/20">
            <div className="bg-[#10F0A0] h-full rounded-full transition-all shadow-[0_0_10px_#10F0A0]" style={{ width: `${completionPercent}%` }} />
          </div>
        </EcoCard>
      </div>

      {/* Main Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Emission Trend Line Area Chart */}
        <div className="lg:col-span-2 cyber-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-lg font-bold text-white tracking-wide">Historical Emission Trend</h2>
              <p className="text-xs font-mono text-gray-400">30-day carbon trajectory (kg CO₂e)</p>
            </div>
            <span className="text-xs font-mono px-2.5 py-1 rounded-md bg-emerald-950/80 text-[#10F0A0] border border-emerald-500/30">
              -5.2% vs last month
            </span>
          </div>
          <TrendChart data={trendData} />
        </div>

        {/* Category Breakdown Pie Chart */}
        <div className="cyber-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-lg font-bold text-white tracking-wide">Category Breakdown</h2>
              <p className="text-xs font-mono text-gray-400">Emissions by source</p>
            </div>
          </div>
          <BreakdownChart data={chartData} />
        </div>
      </div>

      {/* IoT Live Sensor Telemetry Feed */}
      <div className="cyber-card rounded-2xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <Cpu className="w-5 h-5 text-[#10F0A0]" />
            <h2 className="text-lg font-bold text-white tracking-wide">IoT Telemetry Node Monitors</h2>
          </div>
          <span className="text-xs font-mono text-cyan-400 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
            4 Active Sensors
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {iotStatus.map((sensor) => (
            <div key={sensor.id} className="p-4 rounded-xl bg-[#090e11]/80 border border-emerald-500/20 hover:border-emerald-500/40 transition">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono text-gray-400 uppercase">{sensor.id}</span>
                <span className="text-[10px] font-mono text-[#10F0A0] bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-500/30">ONLINE</span>
              </div>
              <p className="text-sm font-semibold text-gray-200 line-clamp-1 mb-2">{sensor.name}</p>
              <div className="flex items-baseline justify-between">
                <span className={`text-lg font-bold font-mono ${sensor.glow}`}>{sensor.value}</span>
                <span className="text-[11px] font-mono text-gray-500">Realtime</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
