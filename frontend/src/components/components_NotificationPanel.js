import React, { useState, useEffect } from 'react';
import axios from 'axios';

function NotificationPanel() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/users/notifications') // נדרש להוסיף API מתאים
      .then(res => setNotifications(res.data));
  }, []);

  return (
    <div>
      <h2>התראות</h2>
      {notifications.length === 0 ? (
        <p>אין התראות חדשות.</p>
      ) : (
        <ul>
          {notifications.map(n => (
            <li key={n.id}>{n.message} ({n.sent_at})</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default NotificationPanel;