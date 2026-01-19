import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Home, Leaf, Building, Settings, LogOut, ChevronLeft, ChevronRight } from 'lucide-react'
import { useAuthStore } from '../stores/store'

export default function Sidebar() {
  const location = useLocation()
  const logout = useAuthStore((state) => state.logout)
  const [collapsed, setCollapsed] = useState(false)

  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Emissions', href: '/emissions', icon: Leaf },
    { name: 'Campus', href: '/campus', icon: Building },
    { name: 'Settings', href: '/settings', icon: Settings },
  ]

  return (
    <aside
      className={`${
        collapsed ? 'w-20' : 'w-64'
      } bg-gradient-to-b from-primary to-secondary text-white shadow-lg transition-all duration-300 fixed h-screen p-4 flex flex-col`}
    >
      <div className="mb-8 text-center">
        <div className="text-4xl mb-2">
          <Leaf className="w-8 h-8 inline" />
        </div>
        {!collapsed && <h1 className="font-bold text-lg">EcoCampus</h1>}
      </div>

      <nav className="flex-1 space-y-2 px-4">
        {navigation.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.href
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`flex items-center gap-3 p-3 rounded-xl transition-all duration-300 ${
                isActive
                  ? 'bg-white bg-opacity-20'
                  : 'hover:bg-white hover:bg-opacity-10'
              }`}
            >
              <span className="text-xl">
                <Icon className="w-5 h-5 inline" />
              </span>
              {!collapsed && <span>{item.name}</span>}
            </Link>
          )
        })}
      </nav>

      {/* Toggle Button - Before Logout */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="w-full p-3 mb-4 bg-white bg-opacity-10 rounded-xl hover:bg-opacity-20 text-white transition-all"
      >
        {collapsed ? <ChevronRight className="w-5 h-5 mx-auto" /> : <ChevronLeft className="w-5 h-5 mx-auto" />}
      </button>

      {/* Logout Button */}
      <div className="border-t border-white border-opacity-20 pt-4">
        <button
          onClick={logout}
          className="flex items-center gap-2 w-full px-4 py-2 text-sm hover:bg-white hover:bg-opacity-10 rounded-lg transition-colors"
        >
          <LogOut className="w-5 h-5" />
          {!collapsed && <span>Logout</span>}
        </button>
      </div>
    </aside>
  )
}
