import React, { useEffect } from 'react'
import { useAuthStore } from '../stores/store'

export default function Navbar() {
  const user = useAuthStore((state) => state.user)

  return (
    <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center">
      <div>
        <h2 className="text-xl font-semibold text-gray-800">EcoCampus Dashboard</h2>
        <p className="text-sm text-gray-600">Real-time Carbon Tracking System</p>
      </div>
      
      <div className="flex items-center gap-4">
        {user && (
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center text-white font-bold">
              {user.email?.charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">{user.email}</p>
              <p className="text-xs text-gray-500">{user.role || 'User'}</p>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
