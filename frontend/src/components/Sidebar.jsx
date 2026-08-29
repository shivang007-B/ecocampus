import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Home, Leaf, Building, Settings, LogOut, ChevronLeft, ChevronRight, Zap } from 'lucide-react'
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
      } bg-[#0c1317]/95 backdrop-blur-xl border-r border-emerald-500/20 text-white shadow-2xl transition-all duration-300 fixed left-0 top-0 h-screen p-4 flex flex-col z-20`}
    >
      {/* Brand Header */}
      <div className="mb-8 pt-2 flex items-center gap-3 px-2">
        <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-500/40 flex items-center justify-center text-[#10F0A0] shadow-[0_0_15px_rgba(16,240,160,0.25)] shrink-0">
          <Leaf className="w-6 h-6 animate-pulse" />
        </div>
        {!collapsed && (
          <div>
            <h1 className="font-bold text-base tracking-wider text-white flex items-center gap-1">
              ECO<span className="text-[#10F0A0]">CAMPUS</span>
            </h1>
            <p className="text-[10px] font-mono text-emerald-400/70 tracking-widest uppercase">Cyber-Green System</p>
          </div>
        )}
      </div>

      {/* Nav Links */}
      <nav className="flex-1 space-y-2">
        {navigation.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.href
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`flex items-center gap-3.5 px-3.5 py-3 rounded-xl font-medium text-sm transition-all duration-200 ${
                isActive
                  ? 'bg-emerald-950/70 border border-emerald-500/50 text-[#10F0A0] shadow-[0_0_15px_rgba(16,240,160,0.15)] font-semibold'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-emerald-950/30 hover:border hover:border-emerald-500/20'
              }`}
            >
              <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'text-[#10F0A0] drop-shadow-[0_0_8px_rgba(16,240,160,0.6)]' : 'text-gray-400'}`} />
              {!collapsed && <span>{item.name}</span>}
            </Link>
          )
        })}
      </nav>

      {/* Collapse Toggle */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="w-full p-2.5 mb-3 bg-[#131c21] border border-emerald-500/20 rounded-xl hover:border-emerald-500/40 text-gray-300 hover:text-[#10F0A0] transition-all flex items-center justify-center"
        title="Toggle Sidebar"
      >
        {collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
      </button>

      {/* Logout */}
      <div className="border-t border-emerald-500/20 pt-4">
        <button
          onClick={logout}
          className="flex items-center gap-3 w-full px-3.5 py-2.5 text-sm font-mono text-rose-400 hover:text-rose-300 hover:bg-rose-950/30 border border-transparent hover:border-rose-500/30 rounded-xl transition-all"
        >
          <LogOut className="w-5 h-5 shrink-0" />
          {!collapsed && <span>Logout</span>}
        </button>
      </div>
    </aside>
  )
}
