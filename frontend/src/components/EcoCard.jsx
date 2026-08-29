import React from 'react'

export default function EcoCard({ title, value, icon: Icon, children, subtitle, trend }) {
  return (
    <div className="cyber-card rounded-2xl p-6 relative overflow-hidden group">
      {/* Decorative Cyber Accent Line */}
      <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-emerald-500/50 via-teal-400/50 to-transparent group-hover:from-[#10F0A0] transition-all" />
      
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-mono text-emerald-400/80 uppercase tracking-wider mb-1">{title}</p>
          <div className="flex items-baseline gap-2">
            <p className="text-2xl md:text-3xl font-bold text-white font-mono tracking-tight">{value}</p>
            {subtitle && <span className="text-xs font-mono text-gray-400">{subtitle}</span>}
          </div>
          {trend && (
            <p className={`text-xs font-mono mt-2 flex items-center gap-1 ${trend.startsWith('-') ? 'text-emerald-400' : 'text-amber-400'}`}>
              <span>{trend}</span> vs last period
            </p>
          )}
        </div>
        {Icon && (
          <div className="w-12 h-12 rounded-xl bg-emerald-950/60 border border-emerald-500/30 flex items-center justify-center text-[#10F0A0] shadow-[0_0_12px_rgba(16,240,160,0.2)] group-hover:scale-105 transition-transform">
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>
      {children && <div className="mt-4 pt-4 border-t border-emerald-500/10">{children}</div>}
    </div>
  )
}