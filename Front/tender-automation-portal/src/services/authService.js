import axios from 'axios';

// Define API base URL - change this to your Flask backend URL
const API_BASE_URL = 'http://127.0.0.1:5000';

// Axios instance with default headers
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include token in requests
apiClient.interceptors.request.use(
  (config) => {
    // Get token from storage (localStorage or sessionStorage)
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Login service
export const login = async (email, password) => {
  try {
    const response = await apiClient.post('/login', { email, password });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data) {
      throw new Error(error.response.data.message || 'Login failed');
    }
    throw new Error('Network error. Please try again later.');
  }
};

// Logout service
export const logout = () => {
  localStorage.removeItem('token');
  sessionStorage.removeItem('token');
  // Redirect to login page can be handled by the component calling this function
};

// Get user profile service
export const getUserProfile = async () => {
  try {
    const response = await apiClient.get('/user/profile');
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      // Token expired or invalid, perform logout
      logout();
      throw new Error('Session expired. Please login again.');
    }
    throw error;
  }
};
