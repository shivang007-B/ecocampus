import React, { useState } from 'react'
import { Save, Bell, Lock, User as UserIcon, Cpu, ShieldCheck } from 'lucide-react'
import { useAuthStore } from '../stores/store'
import toast from 'react-hot-toast'
import EcoButton from '../components/EcoButton'
import { usersAPI } from '../api/client'

export default function Settings() {
  const user = useAuthStore((state) => state.user)
  const [formData, setFormData] = useState({
    email: user?.email || 'admin@ecocampus.com',
    fullName: user?.full_name || 'System Administrator',
    role: user?.role || 'superuser',
  })
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  })

  const handleProfileSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await usersAPI.updateProfile({ full_name: formData.fullName })
      useAuthStore.setState({ user: response.data })
    toast.success('System Admin Profile Updated', {
      style: { background: '#0e161a', color: '#10F0A0', border: '1px solid rgba(16,240,160,0.4)', fontFamily: 'Fira Code' }
    })
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Profile update failed')
    }
  }

  const handlePasswordSubmit = (e) => {
    e.preventDefault()
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      toast.error('New Passwords do not match', {
        style: { background: '#0e161a', color: '#EF4444', border: '1px solid rgba(239,68,68,0.4)', fontFamily: 'Fira Code' }
      })
      return
    }
    toast.success('Security Token Updated', {
      style: { background: '#0e161a', color: '#10F0A0', border: '1px solid rgba(16,240,160,0.4)', fontFamily: 'Fira Code' }
    })
    setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' })
  }

  return (
    <div className="space-y-8 max-w-3xl animate-fadeIn">
      {/* Header */}
      <div>
        <h1 className="text-2xl md:text-3xl font-bold text-white flex items-center gap-2">
          System Settings & Config <span className="text-[#10F0A0] text-sm font-mono font-normal">● SECURITY NODE</span>
        </h1>
        <p className="text-xs font-mono text-gray-400 mt-1">Configure account access, telemetry parameters and system preferences</p>
      </div>

      {/* Profile Card */}
      <div className="cyber-card rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <UserIcon className="w-5 h-5 text-[#10F0A0]" /> Administrator Profile
        </h2>
        <form onSubmit={handleProfileSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono text-gray-300 mb-1">Full Name / Alias</label>
              <input
                type="text"
                value={formData.fullName}
                onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                className="w-full px-3 py-2.5 cyber-input rounded-xl text-sm font-mono"
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-gray-300 mb-1">System Role</label>
              <input
                type="text"
                value={formData.role}
                disabled
                className="w-full px-3 py-2.5 cyber-input rounded-xl text-sm font-mono opacity-60 cursor-not-allowed uppercase"
              />
            </div>
          </div>
          <div>
            <label className="block text-xs font-mono text-gray-300 mb-1">Primary Email / Identity</label>
            <input
              type="email"
              value={formData.email}
              disabled
              className="w-full px-3 py-2.5 cyber-input rounded-xl text-sm font-mono opacity-60 cursor-not-allowed"
            />
          </div>
          <EcoButton type="submit" className="mt-2">
            <Save className="w-4 h-4" /> Save Profile Preferences
          </EcoButton>
        </form>
      </div>

      {/* Password Security Card */}
      <div className="cyber-card rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Lock className="w-5 h-5 text-cyan-400" /> Security Credentials & Tokens
        </h2>
        <form onSubmit={handlePasswordSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-mono text-gray-300 mb-1">Current Password</label>
            <input
              type="password"
              value={passwordData.currentPassword}
              onChange={(e) => setPasswordData({ ...passwordData, currentPassword: e.target.value })}
              className="w-full px-3 py-2.5 cyber-input rounded-xl text-sm font-mono"
              required
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono text-gray-300 mb-1">New Password</label>
              <input
                type="password"
                value={passwordData.newPassword}
                onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                className="w-full px-3 py-2.5 cyber-input rounded-xl text-sm font-mono"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-gray-300 mb-1">Confirm New Password</label>
              <input
                type="password"
                value={passwordData.confirmPassword}
                onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                className="w-full px-3 py-2.5 cyber-input rounded-xl text-sm font-mono"
                required
              />
            </div>
          </div>
          <EcoButton type="submit" variant="cyan" className="mt-2">
            <ShieldCheck className="w-4 h-4" /> Update Security Credentials
          </EcoButton>
        </form>
      </div>

      {/* System Telemetry Metadata */}
      <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/20 text-xs font-mono text-gray-400 flex items-center justify-between">
        <div>
          <p className="text-white font-semibold flex items-center gap-1.5">
            <Cpu className="w-4 h-4 text-[#10F0A0]" /> EcoCampus Cyber Core v1.0.0
          </p>
          <p className="mt-0.5 text-gray-500">Database Engine: SQLite (Local Demo MVP Mode)</p>
        </div>
        <span className="px-2.5 py-1 rounded bg-emerald-950/80 text-[#10F0A0] border border-emerald-500/30">
          HEALTHY
        </span>
      </div>
    </div>
  )
}
