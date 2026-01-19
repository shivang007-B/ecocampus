import React from 'react'
import { Navigate } from 'react-router-dom'
import { Outlet } from 'react-router-dom'
import { useAuthStore } from '../stores/store'

export default function PrivateRoute() {
  const token = useAuthStore((state) => state.token)

  return token ? <Outlet /> : <Navigate to="/login" replace />
}
