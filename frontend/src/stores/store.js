import { create } from 'zustand';
import { authAPI } from '../api/client';

export const useAuthStore = create((set) => ({
  user: JSON.parse(localStorage.getItem('user')) || null,
  token: localStorage.getItem('token') || null,
  isLoading: false,
  error: null,

  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authAPI.login(email, password);
      const { user, access_token } = response.data;
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      set({ user, token: access_token, isLoading: false });
      return response.data;
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Login failed';
      set({ error: errorMsg, isLoading: false });
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    set({ user: null, token: null });
    authAPI.logout();
  },

  setUser: (user) => set({ user }),
}));

export const useCarbonStore = create((set) => ({
  emissions: [],
  trends: [],
  goals: [],
  isLoading: false,

  setEmissions: (emissions) => set({ emissions }),
  setTrends: (trends) => set({ trends }),
  setGoals: (goals) => set({ goals }),
  setIsLoading: (isLoading) => set({ isLoading }),
}));

export const useCampusStore = create((set) => ({
  campuses: [],
  selectedCampus: null,
  isLoading: false,

  setCampuses: (campuses) => set({ campuses }),
  setSelectedCampus: (selectedCampus) => set({ selectedCampus }),
  setIsLoading: (isLoading) => set({ isLoading }),
}));

export const useIoTStore = create((set) => ({
  devices: [],
  deviceData: {},
  isLoading: false,

  setDevices: (devices) => set({ devices }),
  setDeviceData: (deviceData) => set({ deviceData }),
  setIsLoading: (isLoading) => set({ isLoading }),
}));
