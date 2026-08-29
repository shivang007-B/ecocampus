import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Leaf, Mail, Lock, ShieldCheck, Cpu } from 'lucide-react'
import { useAuthStore } from '../stores/store'
import toast from 'react-hot-toast'
import EcoButton from '../components/EcoButton'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const login = useAuthStore((state) => state.login)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      await login(email, password)
      toast.success('Access Granted - Cyber Telemetry Active', {
        style: {
          background: '#0e161a',
          color: '#10F0A0',
          border: '1px solid rgba(16,240,160,0.4)',
          fontFamily: 'Fira Code'
        }
      })
      navigate('/')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Authentication Failed', {
        style: {
          background: '#0e161a',
          color: '#EF4444',
          border: '1px solid rgba(239,68,68,0.4)',
          fontFamily: 'Fira Code'
        }
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#080c0e] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Cyber Glow Effects */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="cyber-card rounded-2xl max-w-md w-full p-8 relative z-10 border border-emerald-500/30 shadow-[0_0_50px_rgba(0,0,0,0.8)]">
        {/* Header Icon */}
        <div className="flex justify-center mb-6">
          <div className="w-16 h-16 rounded-2xl bg-emerald-950/80 border border-emerald-500/40 flex items-center justify-center text-[#10F0A0] shadow-[0_0_20px_rgba(16,240,160,0.3)]">
            <Leaf className="w-8 h-8 animate-pulse" />
          </div>
        </div>
        
        <h1 className="text-2xl md:text-3xl font-bold text-center text-white mb-1 tracking-wider">
          ECO<span className="text-[#10F0A0]">CAMPUS</span>
        </h1>
        <p className="text-center text-xs font-mono text-emerald-400/70 mb-8 uppercase tracking-widest">
          GHG Emissions & Telemetry Gateway
        </p>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-mono text-gray-300 mb-2 uppercase tracking-wider">
              Identity / Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3.5 top-3 w-4 h-4 text-emerald-500/70" />
              <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@ecocampus.com"
                className="w-full pl-10 pr-4 py-2.5 cyber-input rounded-xl text-sm font-mono focus:ring-0"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-mono text-gray-300 mb-2 uppercase tracking-wider">
              Security Token / Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3.5 top-3 w-4 h-4 text-emerald-500/70" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-4 py-2.5 cyber-input rounded-xl text-sm font-mono focus:ring-0"
                required
              />
            </div>
          </div>

          <EcoButton
            type="submit"
            disabled={isLoading}
            className="w-full py-3 mt-2"
          >
            {isLoading ? 'Authenticating...' : 'INITIALIZE SYSTEM ACCESS'}
          </EcoButton>
        </form>

        {/* Demo Credentials Box */}
        <div className="mt-6 p-4 rounded-xl bg-emerald-950/40 border border-emerald-500/30">
          <div className="flex items-center justify-between gap-2">
            <div>
              <p className="text-[10px] font-mono font-semibold text-[#10F0A0] uppercase tracking-widest mb-1 flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5 inline" /> Demo Credentials
              </p>
              <p className="text-xs font-mono text-gray-300">admin@ecocampus.com</p>
              <p className="text-[11px] font-mono text-gray-400">password: password123</p>
            </div>
            <button
              type="button"
              onClick={() => {
                setEmail('admin@ecocampus.com')
                setPassword('password123')
              }}
              className="px-3 py-1.5 bg-emerald-500/20 hover:bg-emerald-500/40 border border-emerald-500/50 text-[#10F0A0] text-xs font-mono font-semibold rounded-lg shadow-sm transition"
            >
              Fill Demo
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
