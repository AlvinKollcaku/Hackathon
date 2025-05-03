import React, { useState, useEffect } from 'react';
import { logout } from '../services/authService';
import { Plus, Edit, Trash2, Eye, Award, X, FileText, Upload } from 'lucide-react';
import { useNavigate } from 'react-router-dom';


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
      const response = await fetch('{{ _.url }}/tenders');
      if (!response.ok) {
        throw new Error('Failed to fetch tenders');
      }
      const data = await response.json();
      setTenders(data);
      setError(null);
    } catch (err) {
      setError('Error fetching tenders: ' + err.message);
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
      
      const response = await fetch('{{ _.url }}/tenders', {
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
      const response = await fetch(`{{ _.url }}/tenders/${currentTender.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(currentTender),
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
        const response = await fetch(`{{ _.url }}/tenders/${id}`, {
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
      const response = await fetch(`{{ _.url }}/tenders/${tenderId}/bids`);
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
      const response = await fetch(`{{ *.url }}/tenders/${tenderId}/attachments`);
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
      
      const response = await fetch(`{{ *.url }}/tenders/${currentTender.id}/attachments`, {
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
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Procurement Officer Dashboard</h1>
          <button 
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow container mx-auto p-4 md:p-6">
        {/* Error Alert */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 flex justify-between items-center">
            <span>{error}</span>
            <button onClick={() => setError(null)} className="font-bold">×</button>
          </div>
        )}

        {/* Publish Tender Button */}
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-xl font-semibold">All Tenders</h2>
          <button 
            onClick={() => setShowPublishModal(true)}
            className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded flex items-center gap-2"
          >
            <Plus size={16} /> Publish New Tender
          </button>
        </div>

        {/* Tenders Table */}
        {loading ? (
          <div className="text-center py-4">Loading tenders...</div>
        ) : tenders.length > 0 ? (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Deadline</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Budget</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {tenders.map((tender) => (
                  <tr key={tender.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{tender.title}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {tender.description.length > 50 
                        ? `${tender.description.substring(0, 50)}...` 
                        : tender.description}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(tender.deadline).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      ${tender.budget.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                        ${tender.status === 'Open' ? 'bg-green-100 text-green-800' : 
                          tender.status === 'Closed' ? 'bg-red-100 text-red-800' : 
                          'bg-yellow-100 text-yellow-800'}`}>
                        {tender.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button 
                          onClick={() => handleViewTender(tender)}
                          className="text-blue-600 hover:text-blue-900"
                          title="View Details"
                        >
                          <Eye size={18} />
                        </button>
                        <button 
                          onClick={() => handleEditTender(tender)}
                          className="text-yellow-600 hover:text-yellow-900"
                          title="Edit"
                        >
                          <Edit size={18} />
                        </button>
                        <button 
                          onClick={() => handleDeleteTender(tender.id)}
                          className="text-red-600 hover:text-red-900"
                          title="Delete"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-4 bg-white rounded-lg shadow">
            <p className="text-gray-500">No tenders available. Publish a new tender to get started.</p>
          </div>
        )}
      </main>

      {/* Publish Tender Modal */}
      {showPublishModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-lg w-full max-w-md">
            <div className="flex justify-between items-center border-b p-4">
              <h3 className="text-lg font-medium">Publish New Tender</h3>
              <button onClick={() => setShowPublishModal(false)} className="text-gray-400 hover:text-gray-500">
                <X size={20} />
              </button>
            </div>
            <form onSubmit={handlePublishTender} className="p-4">
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="title">
                  Title
                </label>
                <input
                  type="text"
                  id="title"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={newTender.title}
                  onChange={(e) => setNewTender({...newTender, title: e.target.value})}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="description">
                  Description
                </label>
                <textarea
                  id="description"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={newTender.description}
                  onChange={(e) => setNewTender({...newTender, description: e.target.value})}
                  required
                  rows="3"
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="deadline">
                  Deadline
                </label>
                <input
                  type="date"
                  id="deadline"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={newTender.deadline}
                  onChange={(e) => setNewTender({...newTender, deadline: e.target.value})}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="budget">
                  Budget
                </label>
                <input
                  type="number"
                  id="budget"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={newTender.budget}
                  onChange={(e) => setNewTender({...newTender, budget: e.target.value})}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="file">
                  Tender Document
                </label>
                <div className="flex items-center justify-center w-full">
                  <label className="flex flex-col w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      <Upload size={40} className="text-gray-400" />
                      <p className="mt-2 text-sm text-gray-500">
                        {selectedFile ? selectedFile.name : "Click to upload or drag and drop"}
                      </p>
                    </div>
                    <input 
                      id="file" 
                      type="file" 
                      className="hidden"
                      onChange={handleFileChange} 
                    />
                  </label>
                </div>
              </div>
              <div className="flex justify-end pt-4">
                <button
                  type="button"
                  onClick={() => setShowPublishModal(false)}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 py-2 px-4 rounded mr-2"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
                >
                  Publish
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Tender Modal */}
      {showEditModal && currentTender && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-lg w-full max-w-md">
            <div className="flex justify-between items-center border-b p-4">
              <h3 className="text-lg font-medium">Edit Tender</h3>
              <button onClick={() => setShowEditModal(false)} className="text-gray-400 hover:text-gray-500">
                <X size={20} />
              </button>
            </div>
            <form onSubmit={handleUpdateTender} className="p-4">
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="edit-title">
                  Title
                </label>
                <input
                  type="text"
                  id="edit-title"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={currentTender.title}
                  onChange={(e) => setCurrentTender({...currentTender, title: e.target.value})}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="edit-description">
                  Description
                </label>
                <textarea
                  id="edit-description"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={currentTender.description}
                  onChange={(e) => setCurrentTender({...currentTender, description: e.target.value})}
                  required
                  rows="3"
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="edit-deadline">
                  Deadline
                </label>
                <input
                  type="date"
                  id="edit-deadline"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={currentTender.deadline.substring(0, 10)} // Format date for input
                  onChange={(e) => setCurrentTender({...currentTender, deadline: e.target.value})}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="edit-budget">
                  Budget
                </label>
                <input
                  type="number"
                  id="edit-budget"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={currentTender.budget}
                  onChange={(e) => setCurrentTender({...currentTender, budget: e.target.value})}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="edit-status">
                  Status
                </label>
                <select
                  id="edit-status"
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  value={currentTender.status}
                  onChange={(e) => setCurrentTender({...currentTender, status: e.target.value})}
                  required
                >
                  <option value="Open">Open</option>
                  <option value="Closed">Closed</option>
                  <option value="Awarded">Awarded</option>
                </select>
              </div>
              <div className="flex justify-end pt-4">
                <button
                  type="button"
                  onClick={() => setShowEditModal(false)}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 py-2 px-4 rounded mr-2"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded"
                >
                  Update
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Tender Details & Bids Modal */}
      {showBidsModal && currentTender && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-lg w-full max-w-4xl max-h-screen overflow-y-auto">
            <div className="flex justify-between items-center border-b p-4 sticky top-0 bg-white">
              <h3 className="text-lg font-medium">Tender Details: {currentTender.title}</h3>
              <button onClick={() => setShowBidsModal(false)} className="text-gray-400 hover:text-gray-500">
                <X size={20} />
              </button>
            </div>
            
            <div className="p-4">
              <div className="mb-6">
                <h4 className="text-md font-semibold mb-2">Tender Information</h4>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="mb-2"><span className="font-medium">Description:</span> {currentTender.description}</p>
                  <p className="mb-2"><span className="font-medium">Deadline:</span> {new Date(currentTender.deadline).toLocaleDateString()}</p>
                  <p className="mb-2"><span className="font-medium">Budget:</span> ${currentTender.budget.toLocaleString()}</p>
                  <p><span className="font-medium">Status:</span> {currentTender.status}</p>
                </div>
              </div>
              
              {/* Attachments Section */}
              <div className="mb-6">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="text-md font-semibold">Attachments</h4>
                  <form onSubmit={uploadAttachment} className="flex items-center">
                    <input
                      type="file"
                      onChange={handleFileChange}
                      className="text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                    />
                    <button
                      type="submit"
                      className="bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded text-sm flex items-center gap-1"
                    >
                      <Upload size={14} /> Upload
                    </button>
                  </form>
                </div>
                
                {attachments.length > 0 ? (
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <ul className="divide-y divide-gray-200">
                      {attachments.map((attachment) => (
                        <li key={attachment.id} className="py-2 flex justify-between items-center">
                          <div className="flex items-center gap-2">
                            <FileText size={16} className="text-gray-500" />
                            <span>{attachment.fileName}</span>
                          </div>
                          <a 
                            href={attachment.fileUrl} 
                            download
                            className="text-blue-600 hover:text-blue-800 text-sm"
                          >
                            Download
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm italic">No attachments available</p>
                )}
              </div>
              
              {/* Bids Section */}
              <div>
                <h4 className="text-md font-semibold mb-2">Vendor Bids</h4>
                {bids.length > 0 ? (
                  <div className="bg-gray-50 rounded-lg overflow-hidden">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-100">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vendor</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Submission Date</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200">
                        {bids.map((bid) => (
                          <tr key={bid.id}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm">{bid.vendorName}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm">${bid.amount.toLocaleString()}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm">{new Date(bid.submissionDate).toLocaleDateString()}</td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                                ${bid.status === 'Pending' ? 'bg-yellow-100 text-yellow-800' : 
                                  bid.status === 'Accepted' ? 'bg-green-100 text-green-800' : 
                                  'bg-red-100 text-red-800'}`}>
                                {bid.status}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm">
                              {currentTender.status === 'Open' && (
                                <button
                                  onClick={() => handleAwardBid(currentTender.id, bid.id)}
                                  className="bg-green-500 hover:bg-green-600 text-white py-1 px-3 rounded text-xs flex items-center gap-1"
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
                  <p className="text-gray-500 text-sm italic">No bids received yet</p>
                )}
              </div>
              
              {/* Action Buttons */}
              <div className="mt-6 flex justify-end space-x-2">
                {currentTender.status === 'Open' && (
                  <button
                    onClick={() => handleCloseTender(currentTender.id)}
                    className="bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded flex items-center gap-2"
                  >
                    <X size={16} /> Close Tender (No Winner)
                  </button>
                )}
                <button
                  onClick={() => setShowBidsModal(false)}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-800 py-2 px-4 rounded"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gray-100 p-4 text-center text-gray-500 text-sm">
        <p>© {new Date().getFullYear()} Tender Automation Portal | Procurement Officer Dashboard</p>
      </footer>
    </div>)}

export default UserDashboard;