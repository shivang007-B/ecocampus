import React from 'react'

export default function EcoButton({ children, variant = "primary", className = "", ...props }) {
  const baseStyles = "px-5 py-2.5 rounded-xl font-mono text-sm font-semibold tracking-wide transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
  
  const variants = {
    primary: "bg-emerald-500 hover:bg-[#10F0A0] text-slate-950 shadow-[0_0_15px_rgba(16,240,160,0.3)] hover:shadow-[0_0_22px_rgba(16,240,160,0.6)] border border-emerald-400 font-bold",
    secondary: "cyber-button",
    cyan: "bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-[0_0_15px_rgba(0,229,255,0.3)] border border-cyan-400 font-bold",
    outline: "border border-emerald-500/40 text-[#10F0A0] hover:bg-emerald-950/60 hover:border-[#10F0A0]",
    ghost: "text-gray-400 hover:text-[#10F0A0] hover:bg-emerald-950/40",
  }

  return (
    <button className={`${baseStyles} ${variants[variant] || variants.primary} ${className}`} {...props}>
      {children}
    </button>
  )
}