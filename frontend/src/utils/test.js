/**
 * Test API Client Configuration
 * Quick test to verify frontend can connect to backend
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

async function testConnection() {
  try {
    console.log('Testing API connection...');
    console.log(`API URL: ${API_BASE_URL}`);
    
    // Test health endpoint
    const healthResponse = await axios.get(
      'http://localhost:8000/health'
    );
    
    console.log('✓ Backend is running:', healthResponse.data);
    return true;
  } catch (error) {
    console.error('✗ Backend connection failed:', error.message);
    return false;
  }
}

async function testLogin() {
  try {
    console.log('Testing login endpoint...');
    
    const response = await axios.post(
      `${API_BASE_URL}/auth/login`,
      {
        username: 'admin@ecocampus.com',
        password: 'password123'
      }
    );
    
    console.log('✓ Login successful:', response.data);
    return response.data.access_token;
  } catch (error) {
    console.error('✗ Login failed:', error.response?.data?.detail || error.message);
    return null;
  }
}

// Export for use in browser console
window.ecocampusTest = {
  testConnection,
  testLogin,
  apiUrl: API_BASE_URL
};

console.log('EcoCampus Test Tools Available');
console.log('Use: ecocampusTest.testConnection()');
console.log('Use: ecocampusTest.testLogin()');
