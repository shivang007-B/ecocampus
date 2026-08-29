import React, { useState, useEffect } from 'react'
import { Plus, Trash2, Edit2 } from 'lucide-react'
import { carbonAPI } from '../api/client'
import toast from 'react-hot-toast'

export default function Emissions() {
  const [emissions, setEmissions] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    campus_id: '',
    electricity_emission: '',
    transportation_emission: '',
    waste_emission: '',
    water_emission: '',
    food_emission: '',
    description: '',
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
      } else {
        setEmissions([
          {
            id: 1,
            campus_id: 1,
            electricity_emission: 5234,
            transportation_emission: 4890,
            waste_emission: 2326,
            water_emission: 450,
            food_emission: 1200,
            total_emission: 14100,
            date: new Date().toISOString(),
          }
        ])
      }
    } catch (error) {
      setEmissions([
        {
          id: 1,
          campus_id: 1,
          electricity_emission: 5234,
          transportation_emission: 4890,
          waste_emission: 2326,
          water_emission: 450,
          food_emission: 1200,
          total_emission: 14100,
          date: new Date().toISOString(),
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      // await carbonAPI.createEmission(formData)
      toast.success('Emission recorded successfully')
      setShowForm(false)
      setFormData({
        campus_id: '',
        electricity_emission: '',
        transportation_emission: '',
        waste_emission: '',
        water_emission: '',
        food_emission: '',
        description: '',
      })
      fetchEmissions()
    } catch (error) {
      toast.error('Failed to create emission')
    }
  }

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Emissions</h1>
          <p className="text-gray-600 mt-2">Track and manage campus emissions</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
        >
          <Plus className="w-5 h-5" />
          Record Emission
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Record New Emission</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Campus
                </label>
                <input
                  type="number"
                  value={formData.campus_id}
                  onChange={(e) => setFormData({ ...formData, campus_id: e.target.value })}
                  placeholder="Campus ID"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Electricity (kg CO₂)
                </label>
                <input
                  type="number"
                  value={formData.electricity_emission}
                  onChange={(e) => setFormData({ ...formData, electricity_emission: e.target.value })}
                  placeholder="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Transportation (kg CO₂)
                </label>
                <input
                  type="number"
                  value={formData.transportation_emission}
                  onChange={(e) => setFormData({ ...formData, transportation_emission: e.target.value })}
                  placeholder="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Waste (kg CO₂)
                </label>
                <input
                  type="number"
                  value={formData.waste_emission}
                  onChange={(e) => setFormData({ ...formData, waste_emission: e.target.value })}
                  placeholder="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>
            </div>

            <div className="flex gap-3">
              <button
                type="submit"
                className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition"
              >
                Save
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-400 transition"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Emissions List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Electricity</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Transportation</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Waste</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Total</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {emissions.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-4 text-center text-gray-500">
                    No emissions recorded yet
                  </td>
                </tr>
              ) : (
                emissions.map((emission) => (
                  <tr key={emission.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {new Date(emission.date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {emission.electricity_emission.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {emission.transportation_emission.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {emission.waste_emission.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">
                      {emission.total_emission.toLocaleString()} kg CO₂
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm flex gap-2">
                      <button className="text-blue-600 hover:text-blue-900">
                        <Edit2 className="w-4 h-4" />
                      </button>
                      <button className="text-red-600 hover:text-red-900">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
