import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService';
import '../styles/Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      const response = await login(email, password);
      if (response.access_token) {
        // Store token based on remember me preference
        const storageType = rememberMe ? localStorage : sessionStorage;
        storageType.setItem('token', response.access_token);
        
        // Get role from token and redirect to appropriate dashboard directly
        const { jwtDecode } = require('jwt-decode');
        const decoded = jwtDecode(response.access_token);
        const userRole = decoded.role;
        
        console.log("User role from token:", userRole);
        
        // Directly navigate to role-specific dashboard
        if (userRole === 'admin') {
          navigate('/admin');
        } else if (userRole === 'proc_officer') {
          navigate('/user');
        } else if (userRole === 'vendor') {
          navigate('/supplier');
        } else {
          // Fallback to dashboard route which handles routing logic
          navigate('/dashboard');
        }
      }
    } catch (err) {
      console.error("Login error:", err);
      setError(err.message || 'Invalid credentials. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-header">
          <div className="logo-container">
            <div className="icon document-icon">
              <i className="fas fa-file-alt"></i>
            </div>
            <div className="icon shield-icon">
              <i className="fas fa-shield-alt"></i>
            </div>
          </div>
          <h1>Tender Automation Portal</h1>
          <p>Sign in to access your portal dashboard</p>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <div className="input-container">
              <i className="fas fa-envelope"></i>
              <input
                type="email"
                id="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>
          
          <div className="form-group">
            <div className="password-header">
              <label htmlFor="password">Password</label>
              <a href="#" className="forgot-password">Forgot password?</a>
            </div>
            <div className="input-container">
              <i className="fas fa-lock"></i>
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button 
                type="button" 
                className="toggle-password"
                onClick={togglePasswordVisibility}
              >
                <i className={`fas ${showPassword ? "fa-eye-slash" : "fa-eye"}`}></i>
              </button>
            </div>
          </div>
          
          <div className="form-group checkbox-group">
            <input
              type="checkbox"
              id="remember-me"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
            />
            <label htmlFor="remember-me">Remember me</label>
          </div>
          
          <button 
            type="submit" 
            className="sign-in-button"
            disabled={isLoading}
          >
            {isLoading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>
        
        <div className="login-footer">
          <p>Don't have an account? <a href="#">Contact your administrator</a></p>
        </div>
      </div>
      
      <div className="copyright">
        © 2025 Tender Automation System. All rights reserved.
      </div>
    </div>
  );
};

export default Login;