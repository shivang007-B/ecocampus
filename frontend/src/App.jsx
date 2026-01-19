import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './stores/store'

console.log('✅ All imports loaded')

// Lazy load components
const Layout = React.lazy(() => import('./components/Layout').catch(e => { console.error('❌ Layout import error:', e); throw e; }))
const Login = React.lazy(() => import('./pages/Login').catch(e => { console.error('❌ Login import error:', e); throw e; }))
const Dashboard = React.lazy(() => import('./pages/Dashboard').catch(e => { console.error('❌ Dashboard import error:', e); throw e; }))
const Emissions = React.lazy(() => import('./pages/Emissions').catch(e => { console.error('❌ Emissions import error:', e); throw e; }))
const Campus = React.lazy(() => import('./pages/Campus').catch(e => { console.error('❌ Campus import error:', e); throw e; }))
const Settings = React.lazy(() => import('./pages/Settings').catch(e => { console.error('❌ Settings import error:', e); throw e; }))
const PrivateRoute = React.lazy(() => import('./components/PrivateRoute').catch(e => { console.error('❌ PrivateRoute import error:', e); throw e; }))

function App() {
  const token = useAuthStore((state) => state.token)

  return (
    <>
      <Router>
        <React.Suspense fallback={<div style={{padding: '20px'}}>Loading...</div>}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route element={<PrivateRoute />}>
              <Route element={<Layout />}>
                <Route path="/" element={<Dashboard />} />
                <Route path="/emissions" element={<Emissions />} />
                <Route path="/campus" element={<Campus />} />
                <Route path="/settings" element={<Settings />} />
              </Route>
            </Route>
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </React.Suspense>
      </Router>
      <Toaster position="top-right" />
    </>
  )
}

export default App
