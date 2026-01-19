import React, { useState, useEffect } from 'react'
import { TrendingDown, Target, Zap, Droplets } from 'lucide-react'
import { EmissionChart, TrendChart } from '../components/Charts'
import { carbonAPI } from '../api/client'
import toast from 'react-hot-toast'
import EcoCard from '../components/EcoCard'
import EcoButton from '../components/EcoButton'

export default function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalEmissions: 0,
    monthlyTarget: 0,
    electricityEmissions: 0,
    transportationEmissions: 0,
    wasteEmissions: 0,
  })
  const [chartData, setChartData] = useState([])
  const [trendData, setTrendData] = useState([])

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      
      // Simulate data - in real app would fetch from API
      setStats({
        totalEmissions: 12450,
        monthlyTarget: 15000,
        electricityEmissions: 5234,
        transportationEmissions: 4890,
        wasteEmissions: 2326,
      })

      setChartData([
        { name: 'Electricity', value: 5234 },
        { name: 'Transportation', value: 4890 },
        { name: 'Waste', value: 2326 },
      ])

      setTrendData([
        { date: 'Jan 1', emissions: 12000 },
        { date: 'Jan 8', emissions: 12100 },
        { date: 'Jan 15', emissions: 12300 },
        { date: 'Jan 22', emissions: 12450 },
      ])
    } catch (error) {
      toast.error('Failed to fetch dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const StatCard = ({ icon: Icon, title, value, unit }) => (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-2">
            {value.toLocaleString()}
            <span className="text-sm text-gray-500 ml-1">{unit}</span>
          </p>
        </div>
        <div className="bg-green-100 p-3 rounded-full">
          <Icon className="w-6 h-6 text-green-600" />
        </div>
      </div>
    </div>
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
      </div>
    )
  }

  const completionPercent = (stats.totalEmissions / stats.monthlyTarget) * 100

  return (
    <div className="p-8 animate-fadeIn">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-primary">Welcome to EcoCampus 🌱</h1>
        <p className="text-gray-600 mt-2">Track your campus sustainability journey</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          icon={TrendingDown}
          title="Total Emissions"
          value={stats.totalEmissions}
          unit="kg CO₂"
        />
        <StatCard
          icon={Zap}
          title="Electricity"
          value={stats.electricityEmissions}
          unit="kg CO₂"
        />
        <StatCard
          icon={TrendingDown}
          title="Transportation"
          value={stats.transportationEmissions}
          unit="kg CO₂"
        />
        <StatCard
          icon={Droplets}
          title="Waste"
          value={stats.wasteEmissions}
          unit="kg CO₂"
        />
      </div>

      {/* Progress to Target */}
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Monthly Target Progress</h3>
            <p className="text-sm text-gray-600">{stats.totalEmissions.toLocaleString()} / {stats.monthlyTarget.toLocaleString()} kg CO₂</p>
          </div>
          <Target className="w-6 h-6 text-green-600" />
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-gradient-to-r from-green-500 to-green-600 h-3 rounded-full transition-all duration-500"
            style={{ width: `${Math.min(completionPercent, 100)}%` }}
          ></div>
        </div>
        <div className="mt-2 flex justify-between text-sm text-gray-600">
          <span>{completionPercent.toFixed(1)}% complete</span>
          <span>{(stats.monthlyTarget - stats.totalEmissions).toLocaleString()} kg remaining</span>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Emission Breakdown</h3>
          <EmissionChart data={chartData} />
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Emission Trend</h3>
          <TrendChart data={trendData} />
        </div>
      </div>

      {/* Action Section */}
      <div className="bg-white rounded-2xl p-8 shadow-md mt-8">
        <h2 className="text-2xl font-bold text-primary mb-4">Take Action Today</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <EcoButton variant="primary">💡 Energy Challenge</EcoButton>
          <EcoButton variant="secondary">🚴 Commute Green</EcoButton>
          <EcoButton variant="outline">📱 Report Issue</EcoButton>
        </div>
      </div>
    </div>
  )
}
