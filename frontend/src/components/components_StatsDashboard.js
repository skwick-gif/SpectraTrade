import React, { useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';

function StatsDashboard() {
  const [userId, setUserId] = useState('');
  const [stats, setStats] = useState(null);

  const fetchStats = async () => {
    const res = await axios.get(`http://localhost:8000/stats/user/${userId}`);
    setStats(res.data);
  };

  return (
    <div>
      <h2>סטטיסטיקות משתמש</h2>
      <input placeholder="User ID" value={userId} onChange={e => setUserId(e.target.value)} />
      <button onClick={fetchStats}>שלוף סטטיסטיקות</button>
      {stats && (
        <div>
          <Bar
            data={{
              labels: ['רווחים', 'הפסדים', 'סה"כ'],
              datasets: [
                {
                  label: 'ביצועים',
                  data: [stats.wins, stats.losses, stats.total_trades],
                  backgroundColor: ['green', 'red', 'gray']
                }
              ]
            }}
            options={{ responsive: true }}
          />
          <p>רווח ממוצע: {stats.avg_profit}</p>
          <p>שיעור הצלחה: {(stats.win_rate * 100).toFixed(2)}%</p>
          <p>Drawdown מקסימלי: {stats.max_drawdown}</p>
        </div>
      )}
    </div>
  );
}

export default StatsDashboard;