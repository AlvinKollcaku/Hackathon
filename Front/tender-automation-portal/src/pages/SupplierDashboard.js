import React, { useState, useEffect } from 'react';
import { logout } from '../services/authService';
import { useNavigate } from 'react-router-dom';
import './UserDashboard.css';

const SupplierDashboard = () => {
  const navigate = useNavigate();
  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadingTenderId, setUploadingTenderId] = useState(null);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const fetchTenders = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://127.0.0.1:5000/tenders', {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        const errJson = await response.json().catch(() => ({}));
        throw new Error(errJson.msg || response.statusText);
      }
      const data = await response.json();
      setTenders(data.filter(t => t.status === 'Open'));
      setError(null);
    } catch (err) {
      setError('Error fetching tenders: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTenders();
  }, []);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async (tenderId) => {
    if (!selectedFile) return;
    setUploadingTenderId(tenderId);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://127.0.0.1:5000/tenders/${tenderId}/attachments`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });
      if (!response.ok) {
        const errJson = await response.json().catch(() => ({}));
        throw new Error(errJson.msg || response.statusText);
      }
      setSelectedFile(null);
      alert('Document uploaded successfully!');
    } catch (err) {
      setError('Error uploading document: ' + err.message);
    } finally {
      setUploadingTenderId(null);
    }
  };

  return (
    <div className="user-dashboard-bg">
      {/* Header */}
      <header className="user-dashboard-header">
        <div className="user-dashboard-header-content">
          <h1 className="user-dashboard-title">Vendor Dashboard</h1>
          <button onClick={handleLogout} className="user-dashboard-logout">Logout</button>
        </div>
      </header>

      {/* Main Content */}
      <main className="user-dashboard-main">
        {error && <div className="user-dashboard-error">{error}</div>}
        <h2 className="user-dashboard-section-title">Public Tenders</h2>
        <p style={{marginBottom: '1.5rem'}}>Welcome to the Tender Automation Portal's vendor dashboard. You can upload documents to any open tender below.</p>
        {loading ? (
          <div style={{textAlign: 'center', padding: '2rem'}}>Loading tenders...</div>
        ) : tenders.length > 0 ? (
          <table className="user-dashboard-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Deadline</th>
                <th>Budget</th>
                <th>Upload Document</th>
              </tr>
            </thead>
            <tbody>
              {tenders.map((tender) => (
                <tr key={tender.id}>
                  <td>{tender.title}</td>
                  <td>{tender.description.length > 50 ? `${tender.description.substring(0, 50)}...` : tender.description}</td>
                  <td>{new Date(tender.deadline).toLocaleDateString()}</td>
                  <td>${tender.budget.toLocaleString()}</td>
                  <td>
                    <form onSubmit={e => { e.preventDefault(); handleUpload(tender.id); }} style={{display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
                      <input type="file" onChange={handleFileChange} />
                      <button type="submit" className="user-dashboard-btn" disabled={uploadingTenderId === tender.id}>
                        {uploadingTenderId === tender.id ? 'Uploading...' : 'Upload'}
                      </button>
                    </form>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div style={{textAlign: 'center', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', padding: '2rem'}}>
            <p style={{color: '#64748b'}}>No public tenders available at the moment.</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="user-dashboard-footer">
        <p>© {new Date().getFullYear()} Tender Automation Portal | Vendor Dashboard</p>
      </footer>
    </div>
  );
};

export default SupplierDashboard;