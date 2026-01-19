const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = {
  login: `${API_URL}/api/auth/login`,
  dashboard: `${API_URL}/api/dashboard`,
  emissions: `${API_URL}/api/emissions`,
  campus: `${API_URL}/api/campus`,
}

export default API_URL