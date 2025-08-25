import React, { useState } from 'react';
import axios from 'axios';

function UserAuth() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [mode, setMode] = useState('login');
  const [user, setUser] = useState(null);
  const [role, setRole] = useState('trader');

  const handleAuth = async () => {
    const url =
      mode === 'login'
        ? 'http://localhost:8000/users/login'
        : 'http://localhost:8000/users/register';
    const payload =
      mode === 'login'
        ? { username, password }
        : { username, password, email, role };
    const res = await axios.post(url, payload);
    setUser(res.data);
  };

  return (
    <div>
      {!user ? (
        <>
          <h2>{mode === 'login' ? 'כניסה' : 'הרשמה'}</h2>
          <input placeholder="שם משתמש" value={username} onChange={e => setUsername(e.target.value)} />
          <input placeholder="סיסמה" type="password" value={password} onChange={e => setPassword(e.target.value)} />
          {mode === 'register' && (
            <>
              <input placeholder="אימייל" value={email} onChange={e => setEmail(e.target.value)} />
              <select value={role} onChange={e => setRole(e.target.value)}>
                <option value="trader">סוחר</option>
                <option value="admin">מנהל</option>
                <option value="viewer">צופה</option>
              </select>
            </>
          )}
          <button onClick={handleAuth}>{mode === 'login' ? 'כניסה' : 'הרשמה'}</button>
          <button onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
            החלף ל{mode === 'login' ? 'הרשמה' : 'כניסה'}
          </button>
        </>
      ) : (
        <div>
          <p>שלום, {user.username}! ({user.role})</p>
        </div>
      )}
    </div>
  );
}

export default UserAuth;