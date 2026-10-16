import React from 'react'
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer, PieChart, Pie, Cell, AreaChart, Area
} from 'recharts'

const CYBER_COLORS = ['#10F0A0', '#00E5FF', '#F59E0B', '#A855F7', '#EC4899', '#3B82F6']

const CustomTooltip = ({ active, payload, label }) => {
  if (active && Array.isArray(payload) && payload.length) {
    return (
      <div className="bg-[#0e161a]/95 border border-emerald-500/40 p-3 rounded-xl shadow-2xl backdrop-blur-md font-mono text-xs">
        <p className="text-gray-400 font-semibold mb-1">{label}</p>
        {payload.map((entry, idx) => (
          <p key={idx} className="text-[#10F0A0] flex items-center justify-between gap-4 font-bold">
            <span>{entry.name}:</span>
            <span className="text-white">{Number(entry.value).toLocaleString()} kg CO₂</span>
          </p>
        ))}
      </div>
    )
  }
  return null
}

export function EmissionChart({ data = [] }) {
  const safeData = Array.isArray(data) ? data : []
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={safeData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
        <defs>
          <linearGradient id="cyberBarGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#10F0A0" stopOpacity={0.9} />
            <stop offset="100%" stopColor="#059669" stopOpacity={0.4} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
        <XAxis dataKey="name" stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 12, fontFamily: 'Fira Code' }} axisLine={{ stroke: 'rgba(16,240,160,0.2)' }} />
        <YAxis stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 12, fontFamily: 'Fira Code' }} axisLine={{ stroke: 'rgba(16,240,160,0.2)' }} />
        <Tooltip content={<CustomTooltip />} />
        <Bar dataKey="value" fill="url(#cyberBarGradient)" radius={[6, 6, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  )
}

export function TrendChart({ data = [] }) {
  const safeData = Array.isArray(data) ? data : []
  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={safeData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
        <defs>
          <linearGradient id="cyberTrendGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#10F0A0" stopOpacity={0.4} />
            <stop offset="100%" stopColor="#10F0A0" stopOpacity={0.0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
        <XAxis dataKey="date" stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 11, fontFamily: 'Fira Code' }} axisLine={{ stroke: 'rgba(16,240,160,0.2)' }} />
        <YAxis stroke="#9CA3AF" tick={{ fill: '#9CA3AF', fontSize: 11, fontFamily: 'Fira Code' }} axisLine={{ stroke: 'rgba(16,240,160,0.2)' }} />
        <Tooltip content={<CustomTooltip />} />
        <Area type="monotone" dataKey="emissions" stroke="#10F0A0" strokeWidth={2.5} fillOpacity={1} fill="url(#cyberTrendGradient)" />
      </AreaChart>
    </ResponsiveContainer>
  )
}

export function BreakdownChart({ data = [] }) {
  const safeData = Array.isArray(data) ? data : []
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={safeData}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={95}
          paddingAngle={4}
          dataKey="value"
        >
          {safeData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={CYBER_COLORS[index % CYBER_COLORS.length]} stroke="rgba(8,12,14,0.8)" strokeWidth={2} />
          ))}
        </Pie>
        <Tooltip content={<CustomTooltip />} />
        <Legend
          formatter={(value) => <span className="text-gray-300 font-mono text-xs">{value}</span>}
          wrapperStyle={{ paddingTop: 10 }}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
