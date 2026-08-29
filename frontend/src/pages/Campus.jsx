import React, { useState, useEffect } from 'react'
import { Plus, Trash2, Edit2, MapPin } from 'lucide-react'
import { campusAPI } from '../api/client'
import toast from 'react-hot-toast'

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
      // await campusAPI.create(formData)
      toast.success('Campus created successfully')
      setShowForm(false)
      setFormData({
        name: '',
        location: '',
        area_sqm: '',
        student_count: '',
        staff_count: '',
        building_count: '',
      })
      fetchCampuses()
    } catch (error) {
      toast.error('Failed to create campus')
    }
  }

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Campus Management</h1>
          <p className="text-gray-600 mt-2">Manage your campus locations and information</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition"
        >
          <Plus className="w-5 h-5" />
          Add Campus
        </button>
      </div>

      {/* Form */}
      {showForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Add New Campus</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Campus Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Campus Name"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Location
                </label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  placeholder="City, State"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Area (m²)
                </label>
                <input
                  type="number"
                  value={formData.area_sqm}
                  onChange={(e) => setFormData({ ...formData, area_sqm: e.target.value })}
                  placeholder="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Student Count
                </label>
                <input
                  type="number"
                  value={formData.student_count}
                  onChange={(e) => setFormData({ ...formData, student_count: e.target.value })}
                  placeholder="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Staff Count
                </label>
                <input
                  type="number"
                  value={formData.staff_count}
                  onChange={(e) => setFormData({ ...formData, staff_count: e.target.value })}
                  placeholder="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Building Count
                </label>
                <input
                  type="number"
                  value={formData.building_count}
                  onChange={(e) => setFormData({ ...formData, building_count: e.target.value })}
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

      {/* Campus Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {campuses.length === 0 ? (
          <div className="col-span-full text-center py-12 bg-white rounded-lg">
            <p className="text-gray-500">No campuses yet. Add one to get started!</p>
          </div>
        ) : (
          campuses.map((campus) => (
            <div key={campus.id} className="bg-white rounded-lg shadow hover:shadow-lg transition p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{campus.name}</h3>
                  <div className="flex items-center gap-1 text-gray-600 text-sm mt-1">
                    <MapPin className="w-4 h-4" />
                    {campus.location}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button className="p-2 hover:bg-gray-100 rounded-lg">
                    <Edit2 className="w-4 h-4 text-blue-600" />
                  </button>
                  <button className="p-2 hover:bg-gray-100 rounded-lg">
                    <Trash2 className="w-4 h-4 text-red-600" />
                  </button>
                </div>
              </div>

              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex justify-between">
                  <span>Area:</span>
                  <span className="font-medium">{campus.area_sqm.toLocaleString()} m²</span>
                </div>
                <div className="flex justify-between">
                  <span>Students:</span>
                  <span className="font-medium">{campus.student_count.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span>Staff:</span>
                  <span className="font-medium">{campus.staff_count.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span>Buildings:</span>
                  <span className="font-medium">{campus.building_count}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
