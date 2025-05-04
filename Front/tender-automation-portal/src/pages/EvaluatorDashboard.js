import React, { useState, useEffect } from 'react';
import { logout } from '../services/authService';
import { useNavigate } from 'react-router-dom';
import './UserDashboard.css';

const EvaluatorDashboard = () => {
  const navigate = useNavigate();
  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [attachments, setAttachments] = useState([]);
  const [bids, setBids] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentTender, setCurrentTender] = useState(null);

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

  const fetchTenderAttachmentsAndBids = async (tenderId) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(
        `http://127.0.0.1:5000/tenders/${tenderId}/attachments/all`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );
      if (!response.ok) throw new Error('Failed to fetch');
  
      const data = await response.json();  // this is an Array<Attachment>
      // split by owner_type:
      const tenderAttachments = data.filter(att => att.owner_type === 'tender');
      const bidAttachments    = data.filter(att => att.owner_type === 'bid');
  
      setAttachments(tenderAttachments);
      setBids(bidAttachments);
    } catch {
      setAttachments([]);
      setBids([]);
    }
  };
  

  const handleViewTender = async (tender) => {
    setCurrentTender(tender);
    await fetchTenderAttachmentsAndBids(tender.id);
    setShowModal(true);
  };

  useEffect(() => {
    fetchTenders();
  }, []);

  return (
    <div className="user-dashboard-bg">
      {/* Header */}
      <header className="user-dashboard-header">
        <div className="user-dashboard-header-content">
          <h1 className="user-dashboard-title">Evaluator Dashboard</h1>
          <div style={{display: 'flex', gap: '1rem'}}>
            <button onClick={() => navigate('/ai-evaluator')} className="user-dashboard-btn">AI Evaluator</button>
            <button onClick={handleLogout} className="user-dashboard-logout">Logout</button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="user-dashboard-main">
        {error && <div className="user-dashboard-error">{error}</div>}
        <h2 className="user-dashboard-section-title">Published Procurements</h2>
        <p style={{marginBottom: '1.5rem'}}>You can download procurement documents and bids for any open procurement below.</p>
        {loading ? (
          <div style={{textAlign: 'center', padding: '2rem'}}>Loading procurements...</div>
        ) : tenders.length > 0 ? (
          <table className="user-dashboard-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Deadline</th>
                <th>Budget</th>
                <th>Actions</th>
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
                    <button className="user-dashboard-btn" onClick={() => handleViewTender(tender)}>
                      View & Download
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div style={{textAlign: 'center', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', padding: '2rem'}}>
            <p style={{color: '#64748b'}}>No published procurements available at the moment.</p>
          </div>
        )}
      </main>

      {/* Modal for Downloading Documents and Bids */}
      {showModal && currentTender && (
        <div className="user-dashboard-modal-bg">
          <div className="user-dashboard-modal">
            <div className="user-dashboard-modal-header">
              <span className="user-dashboard-modal-title">Procurement Details: {currentTender.title}</span>
              <button onClick={() => setShowModal(false)} className="user-dashboard-modal-close">×</button>
            </div>
            <div className="user-dashboard-modal-content">
              <div className="user-dashboard-modal-section">
                <h4 className="user-dashboard-modal-section-title">Procurement Document(s)</h4>
                {attachments.length > 0 ? (
                  <ul className="user-dashboard-modal-list">
                    {attachments.map((attachment) => (
                      <li key={attachment.id} className="user-dashboard-modal-list-item">
                        <div className="user-dashboard-modal-list-item-content">
                          <span className="user-dashboard-modal-list-item-text">{attachment.file_name}</span>
                          <a href={attachment.file_url} download className="user-dashboard-modal-list-item-link">Download</a>
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="user-dashboard-modal-text-italic">No procurement documents available</p>
                )}
              </div>
              <div className="user-dashboard-modal-section">
                <h4 className="user-dashboard-modal-section-title">Bids</h4>
                {bids.length > 0 ? (
                  <ul className="user-dashboard-modal-list">
                    {bids.map((bid) => (
                      <li key={bid.id} className="user-dashboard-modal-list-item">
                        <div className="user-dashboard-modal-list-item-content">
                          <span className="user-dashboard-modal-list-item-text">{bid.vendorName ? `${bid.vendorName} - ` : ''}{bid.file_name}</span>
                          <a href={bid.file_url} download className="user-dashboard-modal-list-item-link">Download Bid</a>
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="user-dashboard-modal-text-italic">No bids available</p>
                )}
              </div>
              <div className="user-dashboard-modal-actions">
                <button onClick={() => setShowModal(false)} className="user-dashboard-btn">Close</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="user-dashboard-footer">
        <p>© {new Date().getFullYear()} Tender Automation Portal | Evaluator Dashboard</p>
      </footer>
    </div>
  );
};

export default EvaluatorDashboard; 