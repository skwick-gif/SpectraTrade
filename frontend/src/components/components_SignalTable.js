import React, { useEffect, useState } from 'react';
import axios from 'axios';

function SignalTable() {
  const [signals, setSignals] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/trading/signal').then(res => {
      setSignals(res.data);
    });
  }, []);

  return (
    <div>
      <h2>איתותים פעילים</h2>
      <table>
        <thead>
          <tr>
            <th>סימבול</th>
            <th>פעולה</th>
            <th>מחיר</th>
            <th>SL</th>
            <th>TP</th>
            <th>סטטוס</th>
            <th>משתמש</th>
          </tr>
        </thead>
        <tbody>
          {signals.map(s =>
            <tr key={s.id}>
              <td>{s.symbol}</td>
              <td>{s.action}</td>
              <td>{s.price}</td>
              <td>{s.sl}</td>
              <td>{s.tp}</td>
              <td>{s.status}</td>
              <td>{s.user_id}</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default SignalTable;