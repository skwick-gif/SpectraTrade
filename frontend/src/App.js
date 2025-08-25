import React, { useState } from 'react';
import axios from 'axios';
import StockTable from './components/StockTable';

function App() {
  const [symbols, setSymbols] = useState('AAPL,MSFT,GOOG');
  const [data, setData] = useState(null);

  const scanStocks = async () => {
    const res = await axios.get(`http://localhost:8000/screener?symbols=${symbols}`);
    setData(res.data.stocks);
  };

  return (
    <div>
      <h2>Stock Screener</h2>
      <input
        value={symbols}
        onChange={e => setSymbols(e.target.value)}
        style={{ width: 300 }}
      />
      <button onClick={scanStocks}>Scan</button>
      <StockTable stocks={data || []} />
    </div>
  );
}

export default App;