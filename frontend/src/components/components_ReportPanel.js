import React, { useState } from 'react';
import axios from 'axios';

function ReportPanel() {
  const [userId, setUserId] = useState('');
  const [signalId, setSignalId] = useState('');
  const [report, setReport] = useState(null);

  const fetchUserReport = async () => {
    const res = await axios.get(`http://localhost:8000/stats/user/${userId}`);
    setReport(res.data);
  };

  const fetchSignalReport = async () => {
    const res = await axios.get(`http://localhost:8000/stats/signal/${signalId}`);
    setReport(res.data);
  };

  const fetchGlobalReport = async () => {
    const res = await axios.get('http://localhost:8000/stats/global');
    setReport(res.data);
  };

  return (
    <div>
      <h2>דוחות מערכת</h2>
      <input placeholder="User ID" value={userId} onChange={e => setUserId(e.target.value)} />
      <button onClick={fetchUserReport}>דוח לפי משתמש</button>
      <input placeholder="Signal ID" value={signalId} onChange={e => setSignalId(e.target.value)} />
      <button onClick={fetchSignalReport}>דוח לפי איתות</button>
      <button onClick={fetchGlobalReport}>דוח גלובלי</button>
      {report && (
        <div>
          <pre>{JSON.stringify(report, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default ReportPanel;