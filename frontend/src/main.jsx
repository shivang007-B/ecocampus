import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error("❌ React Error Boundary Caught Error:", error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 bg-[#080c0e] text-[#10F0A0] font-mono min-h-screen flex flex-col items-center justify-center text-center">
          <h1 className="text-2xl font-bold mb-4">⚠️ EcoCampus Runtime Notice</h1>
          <p className="text-gray-300 text-sm mb-4">A session or state conflict occurred.</p>
          <pre className="text-rose-400 text-xs bg-black/60 p-4 rounded-xl max-w-xl overflow-x-auto mb-6 text-left border border-rose-500/30">
            {String(this.state.error?.stack || this.state.error)}
          </pre>
          <button 
            onClick={() => { localStorage.clear(); window.location.href = '/login'; }}
            className="px-6 py-2.5 bg-[#10F0A0] text-black font-bold rounded-xl hover:bg-emerald-400 transition"
          >
            Reset Session & Return to Login
          </button>
        </div>
      )
    }
    return this.props.children
  }
}

const rootElement = document.getElementById('root')
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </React.StrictMode>,
  )
}
