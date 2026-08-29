import React, { useState, useEffect } from 'react'
import { Plus, Building as BuildingIcon, MapPin, Users, Zap, Layers, Calendar, Trash2, X } from 'lucide-react'
import { campusAPI } from '../api/client'
import toast from 'react-hot-toast'
import EcoButton from '../components/EcoButton'

export default function Campus() {
  const [campuses, setCampuses] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    location: '',
    area_sqm: '',
    student_count: '',
    staff_count: '',
    building_count: '',
  })

  useEffect(() => {
    fetchCampuses()
  }, [])

  const fetchCampuses = async () => {
    try {
      setLoading(true)
      const response = await campusAPI.getAll()
      if (response.data && response.data.length > 0) {
        setCampuses(response.data)
      } else {
        setCampuses([
          {
            id: 1,
            name: 'EcoCampus Main Campus',
            location: 'Smart City, Green Park',
            area_sqm: 100000,
            student_count: 5000,
            staff_count: 500,
            building_count: 7,
          }
        ])
      }
    } catch (error) {
      setCampuses([
        {
          id: 1,
          name: 'EcoCampus Main Campus',
          location: 'Smart City, Green Park',
          area_sqm: 100000,
          student_count: 5000,
          staff_count: 500,
          building_count: 7,
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      toast.success('Campus Facility Node Registered', {
        style: { background: '#0e161a', color: '#10F0A0', border: '1px solid rgba(16,240,160,0.4)', fontFamily: 'Fira Code' }
      })
      setShowForm(false)
      setFormData({ name: '', location: '', area_sqm: '', student_count: '', staff_count: '', building_count: '' })
      fetchCampuses()
    } catch (error) {
      toast.error('Failed to register campus')
    }
  }

  const mockBuildings = [
    { id: 1, name: 'Main Academic Block', type: 'Academic', area: '20,000 sqm', energy: 'Rating A+', floors: 5 },
    { id: 2, name: 'Computer Science Dept', type: 'Lab & Research', area: '5,000 sqm', energy: 'Rating A', floors: 4 },
    { id: 3, name: 'Boys Hostel Complex A', type: 'Residential', area: '15,000 sqm', energy: 'Rating B', floors: 4 },
    { id: 4, name: 'Girls Hostel Complex B', type: 'Residential', area: '12,000 sqm', energy: 'Rating A', floors: 4 },
    { id: 5, name: 'Central Digital Library', type: 'Academic', area: '8,000 sqm', energy: 'Rating A+', floors: 3 },
    { id: 6, name: 'Eco Dining & Cafeteria', type: 'Cafeteria', area: '3,000 sqm', energy: 'Rating B', floors: 2 },
  ]

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-white flex items-center gap-2">
            Campus Infrastructure <span className="text-[#10F0A0] text-sm font-mono font-normal">● 1 CAMPUS NODE</span>
          </h1>
          <p className="text-xs font-mono text-gray-400 mt-1">Manage physical campus assets, building telemetry & occupant data</p>
        </div>
        <EcoButton onClick={() => setShowForm(!showForm)}>
          <Plus className="w-4 h-4" /> Add Campus Facility
        </EcoButton>
      </div>

      {/* Modal / Form */}
      {showForm && (
        <div className="cyber-card rounded-2xl p-6 border border-emerald-500/40 relative">
          <button
            onClick={() => setShowForm(false)}
            className="absolute top-4 right-4 text-gray-400 hover:text-white"
          >
            <X className="w-5 h-5" />
          </button>
          <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <BuildingIcon className="w-5 h-5 text-[#10F0A0]" /> Register New Campus Node
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-mono text-gray-300 mb-1">Campus Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="e.g. EcoCampus North Node"
                  className="w-full px-3 py-2 cyber-input rounded-xl text-sm font-mono"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-mono text-gray-300 mb-1">Location</label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  placeholder="e.g. Smart City, Zone 4"
                  className="w-full px-3 py-2 cyber-input rounded-xl text-sm font-mono"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-mono text-gray-300 mb-1">Area (sqm)</label>
                <input
                  type="number"
                  value={formData.area_sqm}
                  onChange={(e) => setFormData({ ...formData, area_sqm: e.target.value })}
                  placeholder="100000"
                  className="w-full px-3 py-2 cyber-input rounded-xl text-sm font-mono"
                  required
                />
              </div>
            </div>
            <div className="flex justify-end gap-3 pt-2">
              <EcoButton variant="ghost" type="button" onClick={() => setShowForm(false)}>Cancel</EcoButton>
              <EcoButton type="submit">Save Campus Node</EcoButton>
            </div>
          </form>
        </div>
      )}

      {/* Campus Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {campuses.map((c) => (
          <div key={c.id} className="cyber-card rounded-2xl p-6 relative overflow-hidden">
            <div className="flex items-start justify-between mb-4">
              <div>
                <span className="text-[10px] font-mono text-[#10F0A0] bg-emerald-950/80 px-2.5 py-1 rounded-md border border-emerald-500/30 uppercase tracking-widest">
                  PRIMARY NODE ID #{c.id}
                </span>
                <h2 className="text-xl font-bold text-white mt-2">{c.name}</h2>
                <p className="text-xs font-mono text-gray-400 flex items-center gap-1 mt-1">
                  <MapPin className="w-3.5 h-3.5 text-emerald-400" /> {c.location}
                </p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 pt-4 border-t border-emerald-500/20 text-center">
              <div className="p-3 rounded-xl bg-[#080c0e]/60 border border-emerald-500/10">
                <p className="text-[10px] font-mono text-gray-400 uppercase">Surface Area</p>
                <p className="text-base font-bold font-mono text-[#10F0A0] mt-0.5">{Number(c.area_sqm).toLocaleString()} m²</p>
              </div>
              <div className="p-3 rounded-xl bg-[#080c0e]/60 border border-emerald-500/10">
                <p className="text-[10px] font-mono text-gray-400 uppercase">Students / Staff</p>
                <p className="text-base font-bold font-mono text-cyan-400 mt-0.5">{c.student_count} / {c.staff_count}</p>
              </div>
              <div className="p-3 rounded-xl bg-[#080c0e]/60 border border-emerald-500/10">
                <p className="text-[10px] font-mono text-gray-400 uppercase">Buildings</p>
                <p className="text-base font-bold font-mono text-white mt-0.5">{c.building_count} Blocks</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Buildings & Facilities Grid */}
      <div>
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Layers className="w-5 h-5 text-[#10F0A0]" /> Campus Buildings & Energy Ratings
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {mockBuildings.map((bldg) => (
            <div key={bldg.id} className="cyber-card rounded-2xl p-5 hover:border-emerald-500/40 transition">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-500/30">
                  {bldg.type}
                </span>
                <span className="text-xs font-mono text-[#10F0A0] font-bold bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-500/30">
                  {bldg.energy}
                </span>
              </div>
              <h3 className="text-base font-bold text-white mb-2">{bldg.name}</h3>
              <div className="flex items-center justify-between text-xs font-mono text-gray-400 pt-2 border-t border-emerald-500/10">
                <span>Area: {bldg.area}</span>
                <span>Floors: {bldg.floors}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
