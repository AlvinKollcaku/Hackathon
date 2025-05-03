import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserDashboard.css';

const AIEvaluator = () => {
  const navigate = useNavigate();
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFile1Change = (e) => setFile1(e.target.files[0]);
  const handleFile2Change = (e) => setFile2(e.target.files[0]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);
  
    if (!file1 || !file2) {
      setError('Please upload both documents.');
      return;
    }
  
    setLoading(true);
    try {
      const formData = new FormData();
      // — these names must match what Flask is looking for:
      formData.append('requirements', file1);
      formData.append('bid',          file2);
  
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://127.0.0.1:5000/ai/evaluate-docs', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}` // OK to include auth header
        },
        body: formData                       // do NOT set Content-Type here!
      });
  
      if (!response.ok) {
        const errJson = await response.json().catch(() => ({}));
        // your Flask returns { error: "…" }
        throw new Error(errJson.error || response.statusText);
      }
  
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Error evaluating documents: ' + err.message);
    } finally {
      setLoading(false);
    }
  };  

  return (
    <div className="user-dashboard-bg">
      <header className="user-dashboard-header">
        <div className="user-dashboard-header-content">
          <h1 className="user-dashboard-title">AI Evaluator</h1>
          <button onClick={() => navigate(-1)} className="user-dashboard-logout">Back</button>
        </div>
      </header>
      <main className="user-dashboard-main">
        <h2 className="user-dashboard-section-title">Upload Two Documents for AI Evaluation</h2>
        <form onSubmit={handleSubmit} className="user-dashboard-form" style={{maxWidth: 500, margin: '0 auto'}}>
          <label>Document 1</label>
          <input type="file" onChange={handleFile1Change} />
          <label>Document 2</label>
          <input type="file" onChange={handleFile2Change} />
          <div className="user-dashboard-form-actions">
            <button type="submit" className="user-dashboard-btn" disabled={loading}>
              {loading ? 'Evaluating...' : 'Evaluate'}
            </button>
          </div>
        </form>
        {error && <div className="user-dashboard-error" style={{marginTop: 20}}>{error}</div>}
        {result && (
          <div style={{marginTop: 30, background: '#fff', borderRadius: 8, padding: 20, boxShadow: '0 2px 8px rgba(0,0,0,0.04)'}}>
            <h3 style={{marginBottom: 10}}>AI Evaluation Result</h3>
            <pre style={{whiteSpace: 'pre-wrap', wordBreak: 'break-word'}}>{JSON.stringify(result, null, 2)}</pre>
          </div>
        )}
      </main>
      <footer className="user-dashboard-footer">
        <p>© {new Date().getFullYear()} Tender Automation Portal | AI Evaluator</p>
      </footer>
    </div>
  );
};

export default AIEvaluator; 