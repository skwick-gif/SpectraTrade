import React, { useState } from 'react';
import axios from 'axios';

function TradingPanel() {
  const [symbol, setSymbol] = useState('');
  const [action, setAction] = useState('buy');
  const [price, setPrice] = useState('');
  const [userId, setUserId] = useState('');
  const [amount, setAmount] = useState(1);

  const handleSignal = async () => {
    await axios.post('http://localhost:8000/trading/signal', {
      symbol,
      action,
      price: parseFloat(price),
      user_id: parseInt(userId)
    });
    alert('איתות נשלח!');
  };

  const handleTrade = async () => {
    await axios.post('http://localhost:8000/trading/trade', {
      user_id: parseInt(userId),
      signal_id: 1, // יש לבחור איתות אמיתי
      amount: parseFloat(amount)
    });
    alert('עסקה בוצעה!');
  };

  return (
    <div>
      <h2>פאנל מסחר</h2>
      <input placeholder="סימבול" value={symbol} onChange={e => setSymbol(e.target.value)} />
      <select value={action} onChange={e => setAction(e.target.value)}>
        <option value="buy">קנייה</option>
        <option value="sell">מכירה</option>
      </select>
      <input placeholder="מחיר" value={price} onChange={e => setPrice(e.target.value)} type="number" />
      <input placeholder="User ID" value={userId} onChange={e => setUserId(e.target.value)} type="number" />
      <button onClick={handleSignal}>שלח איתות</button>
      <br />
      <input placeholder="כמות" value={amount} onChange={e => setAmount(e.target.value)} type="number" />
      <button onClick={handleTrade}>בצע עסקה</button>
    </div>
  );
}

export default TradingPanel;