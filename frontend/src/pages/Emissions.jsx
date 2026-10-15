import React, { useState, useEffect } from 'react'
import { Plus, Leaf, Zap, Car, Trash2, Droplets, Utensils, Calendar, Filter, X } from 'lucide-react'
import { carbonAPI } from '../api/client'
import toast from 'react-hot-toast'
import EcoButton from '../components/EcoButton'
import { DEMO_EMISSIONS_LOG } from '../data/demoData'

export default function Emissions() {
  const [emissions, setEmissions] = useState(DEMO_EMISSIONS_LOG)
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [filterCategory, setFilterCategory] = useState('ALL')
  const [formData, setFormData] = useState({
    campus_id: '1',
    electricity_emission: '',
    transportation_emission: '',
    waste_emission: '',
    water_emission: '',
    food_emission: '',
    notes: '',
  })

  useEffect(() => {
    fetchEmissions()
  }, [])

  const fetchEmissions = async () => {
    try {
      setLoading(true)
      const response = await carbonAPI.getEmissions()
      if (response.data && response.data.length > 0) {
        setEmissions(response.data)
      }
      // else keep demo data
    } catch (_) {
      // Backend unavailable – demo data already shown, no error toast
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await carbonAPI.createEmission({
        campus_id: Number(formData.campus_id),
        date: new Date().toISOString(),
        electricity_emission: Number(formData.electricity_emission || 0),
        transportation_emission: Number(formData.transportation_emission || 0),
        waste_emission: Number(formData.waste_emission || 0),
        water_emission: Number(formData.water_emission || 0),
        food_emission: Number(formData.food_emission || 0),
        other_emission: 0,
        data_source: 'manual',
        notes: formData.notes || 'Manual demo entry',
      })
      toast.success('Emission Telemetry Record Added', {
        style: { background: '#0e161a', color: '#10F0A0', border: '1px solid rgba(16,240,160,0.4)', fontFamily: 'Fira Code' }
      })
      setShowForm(false)
      setFormData({ campus_id: '1', electricity_emission: '', transportation_emission: '', waste_emission: '', water_emission: '', food_emission: '', notes: '' })
      fetchEmissions()
    } catch (error) {
      toast.error('Failed to create emission record')
    }
  }

  const visibleEmissions = emissions.filter((item) => {
    if (filterCategory === 'ALL') return true
    const field = filterCategory === 'TRANSPORT' ? 'transportation_emission' : `${filterCategory.toLowerCase()}_emission`
    return Number(item[field]) > 0
  })

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-white flex items-center gap-2">
            Emission Logs & Accounting <span className="text-[#10F0A0] text-sm font-mono font-normal">● SCOPE 1, 2 & 3</span>
          </h1>
          <p className="text-xs font-mono text-gray-400 mt-1">Audit trail of carbon equivalent emissions across all campus operational streams</p>
        </div>
        <EcoButton onClick={() => setShowForm(!showForm)}>
          <Plus className="w-4 h-4" /> Record New Emission Batch
        </EcoButton>
      </div>

      {/* Form Modal */}
      {showForm && (
        <div className="cyber-card rounded-2xl p-6 border border-emerald-500/40 relative">
          <button onClick={() => setShowForm(false)} className="absolute top-4 right-4 text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Leaf className="w-5 h-5 text-[#10F0A0]" /> Log GHG Emission Telemetry
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-mono text-gray-300 mb-1">Electricity (kg CO₂)</label>
                <input
                  type="number"
                  value={formData.electricity_emission}
                  onChange={(e) => setFormData({ ...formData, electricity_emission: e.target.value })}
                  placeholder="5000"
                  className="w-full px-3 py-2 cyber-input rounded-xl text-sm font-mono"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-mono text-gray-300 mb-1">Transport (kg CO₂)</label>
                <input
                  type="number"
                  value={formData.transportation_emission}
                  onChange={(e) => setFormData({ ...formData, transportation_emission: e.target.value })}
                  placeholder="4000"
                  className="w-full px-3 py-2 cyber-input rounded-xl text-sm font-mono"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-mono text-gray-300 mb-1">Waste (kg CO₂)</label>
                <input
                  type="number"
                  value={formData.waste_emission}
                  onChange={(e) => setFormData({ ...formData, waste_emission: e.target.value })}
                  placeholder="2000"
                  className="w-full px-3 py-2 cyber-input rounded-xl text-sm font-mono"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-mono text-gray-300 mb-1">Water (kg CO₂)</label>
                <input
                  type="number"
                  value={formData.water_emission}
                  onChange={(e) => setFormData({ ...formData, water_emission: e.target.value })}
                  placeholder="400"
                  className="w-full px-3 py-2 cyber-input rounded-xl text-sm font-mono"
                />
              </div>
              <div>
                <label className="block text-xs font-mono text-gray-300 mb-1">Food / Catering (kg CO₂)</label>
                <input
                  type="number"
                  value={formData.food_emission}
                  onChange={(e) => setFormData({ ...formData, food_emission: e.target.value })}
                  placeholder="1000"
                  className="w-full px-3 py-2 cyber-input rounded-xl text-sm font-mono"
                />
              </div>
              <div>
                <label className="block text-xs font-mono text-gray-300 mb-1">Notes / Tag</label>
                <input
                  type="text"
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  placeholder="Manual audit batch"
                  className="w-full px-3 py-2 cyber-input rounded-xl text-sm font-mono"
                />
              </div>
            </div>
            <div className="flex justify-end gap-3 pt-2">
              <EcoButton variant="ghost" type="button" onClick={() => setShowForm(false)}>Cancel</EcoButton>
              <EcoButton type="submit">Commit Emission Record</EcoButton>
            </div>
          </form>
        </div>
      )}

      {/* Category Stream Pills */}
      <div className="flex flex-wrap items-center gap-2 font-mono text-xs">
        {['ALL', 'ELECTRICITY', 'TRANSPORT', 'WASTE', 'WATER', 'FOOD'].map((cat) => (
          <button
            key={cat}
            onClick={() => setFilterCategory(cat)}
            className={`px-3.5 py-1.5 rounded-xl transition border ${
              filterCategory === cat
                ? 'bg-emerald-950/80 border-emerald-500/60 text-[#10F0A0] font-bold shadow-[0_0_10px_rgba(16,240,160,0.2)]'
                : 'bg-[#0e161a]/60 border-emerald-500/10 text-gray-400 hover:text-gray-200 hover:border-emerald-500/30'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Emission Telemetry Log Table */}
      <div className="cyber-card rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead className="bg-[#080c0e]/80 border-b border-emerald-500/20 text-gray-400 uppercase tracking-wider">
              <tr>
                <th className="p-4">Batch ID / Date</th>
                <th className="p-4">Electricity</th>
                <th className="p-4">Transport</th>
                <th className="p-4">Waste</th>
                <th className="p-4">Water</th>
                <th className="p-4">Food</th>
                <th className="p-4 text-right">Total (kg CO₂)</th>
                <th className="p-4 text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-emerald-500/10 text-gray-200">
              {visibleEmissions.map((item) => (
                <tr key={item.id} className="hover:bg-emerald-950/20 transition">
                  <td className="p-4 font-semibold text-white">
                    <div>#{item.id} - {new Date(item.date).toLocaleDateString()}</div>
                    <div className="text-[10px] text-gray-500 font-normal">{item.notes || 'Automated batch'}</div>
                  </td>
                  <td className="p-4 text-emerald-400">{item.electricity_emission?.toLocaleString()}</td>
                  <td className="p-4 text-cyan-400">{item.transportation_emission?.toLocaleString()}</td>
                  <td className="p-4 text-amber-400">{item.waste_emission?.toLocaleString()}</td>
                  <td className="p-4 text-blue-400">{item.water_emission?.toLocaleString()}</td>
                  <td className="p-4 text-pink-400">{item.food_emission?.toLocaleString()}</td>
                  <td className="p-4 text-right font-bold text-[#10F0A0] text-sm">
                    {item.total_emission?.toLocaleString()}
                  </td>
                  <td className="p-4 text-center">
                    <span className="px-2.5 py-0.5 rounded-full bg-emerald-950/90 text-[#10F0A0] border border-emerald-500/30 text-[10px] uppercase">
                      VERIFIED
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
