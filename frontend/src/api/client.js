import axios from 'axios';

// Same-origin calls work locally through Vite's proxy and after a Vercel deploy.
// Keeping localhost out of a production bundle avoids requests to a visitor's PC.
const configuredUrl = import.meta.env.VITE_API_URL?.replace(/\/$/, '');
const API_BASE_URL = configuredUrl && !configuredUrl.includes('localhost')
  ? configuredUrl
  : '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth endpoints
export const authAPI = {
  login: (email, password) => apiClient.post('/auth/login', { email, password }),
  signup: (data) => apiClient.post('/auth/register', data),
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

// User endpoints
export const usersAPI = {
  getProfile: () => apiClient.get('/users/me'),
  updateProfile: (data) => apiClient.put('/users/me', data),
  getAll: () => apiClient.get('/users'),
  getById: (id) => apiClient.get(`/users/${id}`),
  delete: (id) => apiClient.delete(`/users/${id}`),
};

// Campus endpoints
export const campusAPI = {
  getAll: () => apiClient.get('/campuses'),
  getById: (id) => apiClient.get(`/campuses/${id}`),
  create: (data) => apiClient.post('/campuses', data),
  update: (id, data) => apiClient.put(`/campuses/${id}`, data),
  delete: (id) => apiClient.delete(`/campuses/${id}`),
  getDashboard: (id) => apiClient.get(`/campuses/${id}/dashboard`),
  getBuildings: (id) => apiClient.get(`/campuses/${id}/buildings`),
};

// Carbon endpoints
export const carbonAPI = {
  getEmissions: () => apiClient.get('/carbon/emissions'),
  getEmissionById: (id) => apiClient.get(`/carbon/emissions/${id}`),
  createEmission: (data) => apiClient.post('/carbon/emissions', data),
  calculate: (data) => apiClient.post('/carbon/calculate', data),
  getTrends: (campusId = 1) => apiClient.get(`/campuses/${campusId}/trends`),
  getGoals: () => apiClient.get('/carbon/goals'),
  getReport: () => apiClient.get('/carbon/report'),
};

// IoT endpoints
export const iotAPI = {
  getDevices: () => apiClient.get('/iot/devices'),
  getDeviceById: (id) => apiClient.get(`/iot/devices/${id}`),
  createDevice: (data) => apiClient.post('/iot/devices', data),
  updateDevice: (id, data) => apiClient.put(`/iot/devices/${id}`, data),
  deleteDevice: (id) => apiClient.delete(`/iot/devices/${id}`),
  getDeviceData: (id) => apiClient.get(`/iot/devices/${id}/data`),
};

export default apiClient;
