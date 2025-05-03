import { jwtDecode } from 'jwt-decode';

// Check if user is authenticated
export const isAuthenticated = () => {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token');
  if (!token) return false;
  
  try {
    const decodedToken = jwtDecode(token);
    return decodedToken.exp * 1000 > Date.now();
  } catch (error) {
    return false;
  }
};

// Get user role from JWT token
export const getUserRole = () => {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token');
  if (!token) return null;
  
  try {
    const decodedToken = jwtDecode(token);
    return decodedToken.role;
  } catch (error) {
    return null;
  }
};

// Get user identity
export const getUserIdentity = () => {
  const token = localStorage.getItem('token') || sessionStorage.getItem('token');
  if (!token) return null;
  
  try {
    const decodedToken = jwtDecode(token);
    return decodedToken.sub; // Assuming the identity is stored in the 'sub' claim
  } catch (error) {
    return null;
  }
};