import React, { useEffect } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { isAuthenticated, getUserRole } from './authUtils';

const ProtectedRoute = ({ children, allowedRoles = [] }) => {
  const authenticated = isAuthenticated();
  const userRole = getUserRole();
  const navigate = useNavigate();
  
  useEffect(() => {
    console.log("Protected route check - authenticated:", authenticated);
    console.log("Protected route check - user role:", userRole);
  }, [authenticated, userRole]);
  
  // If not authenticated, redirect to login
  if (!authenticated) {
    console.log("Not authenticated, redirecting to login");
    return <Navigate to="/login" />;
  }
  
  // If allowedRoles is not empty, check if user has permission
  if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
    console.log(`User role ${userRole} not in allowed roles:`, allowedRoles);
    
    // Directly navigate to role-specific dashboard
    if (userRole === 'admin') {
      return <Navigate to="/admin" />;
    } else if (userRole === 'user') {
      return <Navigate to="/user" />;
    } else if (userRole === 'supplier') {
      return <Navigate to="/supplier" />;
    } else {
      // Fallback
      return <Navigate to="/dashboard" />;
    }
  }
  
  // If children is a function, call it with the user role
  if (typeof children === 'function') {
    return children({ role: userRole });
  }
  
  // Otherwise render children directly
  return children;
};

export default ProtectedRoute;
