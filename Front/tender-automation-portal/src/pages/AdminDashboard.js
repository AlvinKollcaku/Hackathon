import React from 'react';
import { logout } from '../services/authService';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
  const navigate = useNavigate();
  
  const handleLogout = () => {
    logout();
    navigate('/login');
  };
  
  return (
    <div className="dashboard">
      <h1>Admin Dashboard</h1>
      <p>Welcome to the Tender Automation Portal's admin dashboard</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default AdminDashboard;