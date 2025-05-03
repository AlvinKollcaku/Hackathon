import React, { useState, useEffect } from 'react';
import { logout } from '../services/authService';
import { Plus, Edit, Trash2, Eye, Award, X, FileText, Upload } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import './UserDashboard.css';

const UserDashboard = () => {
  const navigate = useNavigate()
  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showPublishModal, setShowPublishModal] = useState(false);
  const [showBidsModal, setShowBidsModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [currentTender, setCurrentTender] = useState(null);
  const [bids, setBids] = useState([]);
  const [attachments, setAttachments] = useState([]);
  
  // Form states
  const [newTender, setNewTender] = useState({
    title: '',
    description: '',
    deadline: '',
    budget: '',
    status: 'Open'
  });
  
  const [selectedFile, setSelectedFile] = useState(null);

  const fetchTenders = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");  // or wherever you store it
      const response = await fetch("http://127.0.0.1:5000/tenders", {
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        // if you prefer cookie-based JWTs:
        // credentials: 'include',
      });
  
      if (!response.ok) {
        // pull out the real error message from the server, if any
        const errJson = await response.json().catch(() => ({}));
        throw new Error(errJson.msg || response.statusText);
      }
  
      const data = await response.json();
      setTenders(data);
      setError(null);
    } catch (err) {
      setError("Error fetching tenders: " + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTenders();
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handlePublishTender = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      
      // Add tender details to formData
      Object.keys(newTender).forEach(key => {
        formData.append(key, newTender[key]);
      });
      
      // Add file if selected
      if (selectedFile) {
        formData.append('file', selectedFile);
      }
      
      const response = await fetch('http://127.0.0.1:5000/tenders', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to publish tender');
      }
      
      await fetchTenders();
      setShowPublishModal(false);
      setNewTender({
        title: '',
        description: '',
        deadline: '',
        budget: '',
        status: 'Open'
      });
      setSelectedFile(null);
    } catch (err) {
      setError('Error publishing tender: ' + err.message);
    }
  };

  const handleUpdateTender = async (e) => {
    e.preventDefault();
    try {
        const { title, description, deadline, budget, status } = currentTender;
const payload = { title, description, deadline, budget };

      const response = await fetch(`http://127.0.0.1:5000/tenders/${currentTender.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      
      if (!response.ok) {
        throw new Error('Failed to update tender');
      }
      
      await fetchTenders();
      setShowEditModal(false);
    } catch (err) {
      setError('Error updating tender: ' + err.message);
    }
  };

  const handleDeleteTender = async (id) => {
    if (window.confirm('Are you sure you want to delete this tender?')) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/tenders/${id}`, {
          method: 'DELETE',
        });
        
        if (!response.ok) {
          throw new Error('Failed to delete tender');
        }
        
        await fetchTenders();
      } catch (err) {
        setError('Error deleting tender: ' + err.message);
      }
    }
  };

  const fetchTenderBids = async (tenderId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/tenders/${tenderId}/bids`);
      if (!response.ok) {
        throw new Error('Failed to fetch bids');
      }
      const data = await response.json();
      setBids(data);
      return data;
    } catch (err) {
      setError('Error fetching bids: ' + err.message);
      return [];
    }
  };

  const fetchTenderAttachments = async (tenderId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/tenders/${tenderId}/attachments`);
      if (!response.ok) {
        throw new Error('Failed to fetch attachments');
      }
      const data = await response.json();
      setAttachments(data);
      return data;
    } catch (err) {
      setError('Error fetching attachments: ' + err.message);
      return [];
    }
  };

  const handleViewTender = async (tender) => {
    setCurrentTender(tender);
    await Promise.all([
      fetchTenderBids(tender.id),
      fetchTenderAttachments(tender.id)
    ]);
    setShowBidsModal(true);
  };

  const handleEditTender = (tender) => {
    setCurrentTender({...tender});
    setShowEditModal(true);
  };

  const handleAwardBid = async (tenderId, bidId) => {
    try {
      const response = await fetch(`{{ *.url }}/tenders/${tenderId}/award`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ bidId }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to award bid');
      }
      
      await fetchTenders();
      setShowBidsModal(false);
    } catch (err) {
      setError('Error awarding bid: ' + err.message);
    }
  };

  const handleCloseTender = async (tenderId) => {
    if (window.confirm('Are you sure you want to close this tender without a winner?')) {
      try {
        const response = await fetch(`{{ *.url }}/tenders/${tenderId}/close`, {
          method: 'POST',
        });
        
        if (!response.ok) {
          throw new Error('Failed to close tender');
        }
        
        await fetchTenders();
        setShowBidsModal(false);
      } catch (err) {
        setError('Error closing tender: ' + err.message);
      }
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const uploadAttachment = async (e) => {
    e.preventDefault();
    if (!selectedFile || !currentTender) return;

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      
      const response = await fetch(`http://127.0.0.1:5000/tenders/${currentTender.id}/attachments`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to upload attachment');
      }
      
      await fetchTenderAttachments(currentTender.id);
      setSelectedFile(null);
    } catch (err) {
      setError('Error uploading attachment: ' + err.message);
    }
  };

  return (
    <div className="user-dashboard-bg">
      {/* Header */}
      <header className="user-dashboard-header">
        <div className="user-dashboard-header-content">
          <h1 className="user-dashboard-title">Tender Management Dashboard</h1>
          <button
            onClick={handleLogout}
            className="user-dashboard-logout"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="user-dashboard-main">
        {/* Error Alert */}
        {error && (
          <div className="user-dashboard-error">
            {error}
          </div>
        )}

        {/* Publish Tender Button */}
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
          <h2 className="user-dashboard-section-title">All Tenders</h2>
          <button
            onClick={() => setShowPublishModal(true)}
            className="user-dashboard-btn"
          >
            <Plus size={20} />
            Publish New Tender
          </button>
        </div>

        {/* Tenders Table */}
        {loading ? (
          <div style={{textAlign: 'center', padding: '2rem'}}>Loading tenders...</div>
        ) : tenders.length > 0 ? (
          <div style={{marginBottom: '2rem'}}>
            <table className="user-dashboard-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Description</th>
                  <th>Deadline</th>
                  <th>Budget</th>
                  <th>Status</th>
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
                      <span className={`user-dashboard-badge ${tender.status === 'Open' ? 'user-dashboard-badge-open' : tender.status === 'Closed' ? 'user-dashboard-badge-closed' : 'user-dashboard-badge-awarded'}`}>
                        {tender.status}
                      </span>
                    </td>
                    <td>
                      <div style={{display: 'flex', gap: '0.5rem'}}>
                        <button onClick={() => handleViewTender(tender)} title="View Details" className="user-dashboard-btn" style={{background: '#fff', color: '#2563eb', border: '1px solid #2563eb', padding: '0.25rem 0.75rem'}}><Eye size={18} /></button>
                        <button onClick={() => handleEditTender(tender)} title="Edit" className="user-dashboard-btn" style={{background: '#fff', color: '#eab308', border: '1px solid #eab308', padding: '0.25rem 0.75rem'}}><Edit size={18} /></button>
                        <button onClick={() => handleDeleteTender(tender.id)} title="Delete" className="user-dashboard-btn" style={{background: '#fff', color: '#ef4444', border: '1px solid #ef4444', padding: '0.25rem 0.75rem'}}><Trash2 size={18} /></button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div style={{textAlign: 'center', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', padding: '2rem'}}>
            <p style={{color: '#64748b'}}>No tenders available. Publish a new tender to get started.</p>
          </div>
        )}
      </main>

      {/* Publish Tender Modal */}
      {showPublishModal && (
        <div className="user-dashboard-modal-bg">
          <div className="user-dashboard-modal">
            <div className="user-dashboard-modal-header">
              <span className="user-dashboard-modal-title">Publish New Tender</span>
              <button onClick={() => setShowPublishModal(false)} className="user-dashboard-modal-close"><X size={20} /></button>
            </div>
            <form onSubmit={handlePublishTender} className="user-dashboard-form">
              <label htmlFor="title">Title</label>
              <input type="text" id="title" value={newTender.title} onChange={(e) => setNewTender({...newTender, title: e.target.value})} required />
              <label htmlFor="description">Description</label>
              <textarea id="description" value={newTender.description} onChange={(e) => setNewTender({...newTender, description: e.target.value})} required rows="3" />
              <label htmlFor="deadline">Deadline</label>
              <input type="date" id="deadline" value={newTender.deadline} onChange={(e) => setNewTender({...newTender, deadline: e.target.value})} required />
              <label htmlFor="budget">Budget</label>
              <input type="number" id="budget" value={newTender.budget} onChange={(e) => setNewTender({...newTender, budget: e.target.value})} required />
              <label htmlFor="file">Tender Document</label>
              <input id="file" type="file" onChange={handleFileChange} style={{marginBottom: '1rem'}} />
              <div className="user-dashboard-form-actions">
                <button type="button" onClick={() => setShowPublishModal(false)} className="user-dashboard-form-cancel">Cancel</button>
                <button type="submit" className="user-dashboard-btn">Publish</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Tender Modal */}
      {showEditModal && currentTender && (
        <div className="user-dashboard-modal-bg">
          <div className="user-dashboard-modal">
            <div className="user-dashboard-modal-header">
              <span className="user-dashboard-modal-title">Edit Tender</span>
              <button onClick={() => setShowEditModal(false)} className="user-dashboard-modal-close"><X size={20} /></button>
            </div>
            <form onSubmit={handleUpdateTender} className="user-dashboard-form">
              <label htmlFor="edit-title">Title</label>
              <input type="text" id="edit-title" value={currentTender.title} onChange={(e) => setCurrentTender({...currentTender, title: e.target.value})} required />
              <label htmlFor="edit-description">Description</label>
              <textarea id="edit-description" value={currentTender.description} onChange={(e) => setCurrentTender({...currentTender, description: e.target.value})} required rows="3" />
              <label htmlFor="edit-deadline">Deadline</label>
              <input type="date" id="edit-deadline" value={currentTender.deadline.substring(0, 10)} onChange={(e) => setCurrentTender({...currentTender, deadline: e.target.value})} required />
              <label htmlFor="edit-budget">Budget</label>
              <input type="number" id="edit-budget" value={currentTender.budget} onChange={(e) => setCurrentTender({...currentTender, budget: e.target.value})} required />
              <label htmlFor="edit-status">Status</label>
              <select id="edit-status" value={currentTender.status} onChange={(e) => setCurrentTender({...currentTender, status: e.target.value})} required>
                <option value="Open">Open</option>
                <option value="Closed">Closed</option>
                <option value="Awarded">Awarded</option>
              </select>
              <div className="user-dashboard-form-actions">
                <button type="button" onClick={() => setShowEditModal(false)} className="user-dashboard-form-cancel">Cancel</button>
                <button type="submit" className="user-dashboard-btn">Update</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Tender Details & Bids Modal */}
      {showBidsModal && currentTender && (
        <div className="user-dashboard-modal-bg">
          <div className="user-dashboard-modal">
            <div className="user-dashboard-modal-header">
              <span className="user-dashboard-modal-title">Tender Details: {currentTender.title}</span>
              <button onClick={() => setShowBidsModal(false)} className="user-dashboard-modal-close"><X size={20} /></button>
            </div>
            
            <div className="user-dashboard-modal-content">
              <div className="user-dashboard-modal-section">
                <h4 className="user-dashboard-modal-section-title">Tender Information</h4>
                <div className="user-dashboard-modal-section-content">
                  <p><span className="user-dashboard-modal-label">Description:</span> {currentTender.description}</p>
                  <p><span className="user-dashboard-modal-label">Deadline:</span> {new Date(currentTender.deadline).toLocaleDateString()}</p>
                  <p><span className="user-dashboard-modal-label">Budget:</span> ${currentTender.budget.toLocaleString()}</p>
                  <p><span className="user-dashboard-modal-label">Status:</span> {currentTender.status}</p>
                </div>
              </div>
              
              {/* Attachments Section */}
              <div className="user-dashboard-modal-section">
                <div className="user-dashboard-modal-section-header">
                  <h4 className="user-dashboard-modal-section-title">Attachments</h4>
                  <form onSubmit={uploadAttachment} className="user-dashboard-modal-section-content">
                    <input
                      type="file"
                      onChange={handleFileChange}
                      className="user-dashboard-modal-input"
                    />
                    <button type="submit" className="user-dashboard-btn">Upload</button>
                  </form>
                </div>
                
                {attachments.length > 0 ? (
                  <div className="user-dashboard-modal-section-content">
                    <ul className="user-dashboard-modal-list">
                      {attachments.map((attachment) => (
                        <li key={attachment.id} className="user-dashboard-modal-list-item">
                          <div className="user-dashboard-modal-list-item-content">
                            <span className="user-dashboard-modal-list-item-text">{attachment.fileName}</span>
                            <a 
                              href={attachment.fileUrl} 
                              download
                              className="user-dashboard-modal-list-item-link"
                            >
                              Download
                            </a>
                          </div>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : (
                  <p className="user-dashboard-modal-text-italic">No attachments available</p>
                )}
              </div>
              
              {/* Bids Section */}
              <div className="user-dashboard-modal-section">
                <h4 className="user-dashboard-modal-section-title">Vendor Bids</h4>
                {bids.length > 0 ? (
                  <div className="user-dashboard-modal-section-content">
                    <table className="user-dashboard-modal-table">
                      <thead>
                        <tr>
                          <th>Vendor</th>
                          <th>Amount</th>
                          <th>Submission Date</th>
                          <th>Status</th>
                          <th>Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        {bids.map((bid) => (
                          <tr key={bid.id} className="user-dashboard-modal-table-row">
                            <td>{bid.vendorName}</td>
                            <td>${bid.amount.toLocaleString()}</td>
                            <td>{new Date(bid.submissionDate).toLocaleDateString()}</td>
                            <td>
                              <span className={`user-dashboard-badge ${bid.status === 'Pending' ? 'user-dashboard-badge-pending' : bid.status === 'Accepted' ? 'user-dashboard-badge-accepted' : 'user-dashboard-badge-rejected'}`}>
                                {bid.status}
                              </span>
                            </td>
                            <td>
                              {currentTender.status === 'Open' && (
                                <button
                                  onClick={() => handleAwardBid(currentTender.id, bid.id)}
                                  className="user-dashboard-btn"
                                >
                                  <Award size={12} /> Award
                                </button>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="user-dashboard-modal-text-italic">No bids received yet</p>
                )}
              </div>
              
              {/* Action Buttons */}
              <div className="user-dashboard-modal-actions">
                {currentTender.status === 'Open' && (
                  <button
                    onClick={() => handleCloseTender(currentTender.id)}
                    className="user-dashboard-btn"
                  >
                    <X size={16} /> Close Tender (No Winner)
                  </button>
                )}
                <button
                  onClick={() => setShowBidsModal(false)}
                  className="user-dashboard-btn"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="user-dashboard-footer">
        <p>© {new Date().getFullYear()} Tender Automation Portal | Procurement Officer Dashboard</p>
      </footer>
    </div>
  );
};

export default UserDashboard;