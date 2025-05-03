import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import AdminDashboard from './pages/AdminDashboard';
import UserDashboard from './pages/UserDashboard';
import SupplierDashboard from './pages/SupplierDashboard';
import EvaluatorDashboard from './pages/EvaluatorDashboard';
import AIEvaluator from './pages/AIEvaluator';
import ProtectedRoute from './utils/ProtectedRoute';
import { isAuthenticated } from './utils/authUtils';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={
            isAuthenticated() ? <Navigate to="/dashboard" /> : <Login />
          } />
          
          <Route path="/dashboard" element={
            <ProtectedRoute>
              {({ role }) => {
                if (role === 'admin') return <Navigate to="/admin" />;
                if (role === 'proc_officer') return <Navigate to="/user" />;
                if (role === 'vendor') return <Navigate to="/supplier" />;
                if (role === 'evaluator') return <Navigate to="/evaluator" />;
                return <Navigate to="/login" />;
              }}
            </ProtectedRoute>
          } />
          
          <Route path="/admin" element={
            <ProtectedRoute allowedRoles={['admin']}>
              <AdminDashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/user" element={
            <ProtectedRoute allowedRoles={['proc_officer']}>
              <UserDashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/supplier" element={
            <ProtectedRoute allowedRoles={['vendor']}>
              <SupplierDashboard />
            </ProtectedRoute>
          } />

          <Route path="/evaluator" element={
            <ProtectedRoute allowedRoles={['evaluator']}>
              <EvaluatorDashboard />
            </ProtectedRoute>
          } />

          <Route path="/ai-evaluator" element={
            <ProtectedRoute allowedRoles={['evaluator']}>
              <AIEvaluator />
            </ProtectedRoute>
          } />
          
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
