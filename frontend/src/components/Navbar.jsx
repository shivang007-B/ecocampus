import React from 'react'
import { useAuthStore } from '../stores/store'
import { Activity, ShieldCheck, Cpu } from 'lucide-react'

export default function Navbar() {
  const user = useAuthStore((state) => state.user)

  return (
    <header className="bg-[#0e161a]/90 backdrop-blur-md border-b border-emerald-500/20 px-6 py-3.5 flex items-center justify-between z-10">
      <div className="flex items-center gap-4">
        <div>
          <h2 className="text-lg font-bold text-white tracking-wide flex items-center gap-2">
            EcoCampus <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-950/80 text-[#10F0A0] border border-emerald-500/30">v1.0 MVP</span>
          </h2>
          <p className="text-xs text-gray-400 font-mono">Real-Time GHG Telemetry Node</p>
        </div>
      </div>
      
      {/* Center Live Ticker */}
      <div className="hidden lg:flex items-center gap-6 text-xs font-mono bg-[#080c0e]/80 px-4 py-1.5 rounded-full border border-emerald-500/20">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[#10F0A0] animate-ping" />
          <span className="text-[#10F0A0] font-semibold">IOT STREAM ONLINE</span>
        </div>
        <span className="text-gray-600">|</span>
        <div className="flex items-center gap-1.5 text-gray-300">
          <Cpu className="w-3.5 h-3.5 text-cyan-400" />
          <span>NODES: 4 ACTIVE</span>
        </div>
        <span className="text-gray-600">|</span>
        <div className="flex items-center gap-1.5 text-gray-300">
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
          <span>LATENCY: 12ms</span>
        </div>
      </div>

      {/* User Controls */}
      <div className="flex items-center gap-4">
        {user && (
          <div className="flex items-center gap-3 bg-[#131d22] px-3.5 py-1.5 rounded-xl border border-emerald-500/25">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-400 to-teal-600 flex items-center justify-center text-slate-950 font-bold font-mono text-sm shadow-[0_0_10px_rgba(16,240,160,0.3)]">
              {user.email?.charAt(0).toUpperCase()}
            </div>
            <div className="text-left hidden sm:block">
              <p className="text-xs font-semibold text-gray-200 font-mono">{user.email}</p>
              <span className="inline-flex items-center gap-1 text-[10px] font-mono text-[#10F0A0] uppercase tracking-wider">
                <ShieldCheck className="w-3 h-3 inline" /> {user.role || 'superuser'}
              </span>
            </div>
          </div>
        )}
      </div>
    </header>
  )
}
