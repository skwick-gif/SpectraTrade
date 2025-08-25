import React from 'react';

function StockTable({ stocks }) {
  if (!stocks.length) return null;
  return (
    <table border="1">
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Price</th>
          <th>Name</th>
        </tr>
      </thead>
      <tbody>
        {stocks.map(stock => (
          <tr key={stock.symbol}>
            <td>{stock.symbol}</td>
            <td>{stock.regularMarketPrice}</td>
            <td>{stock.shortName}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default StockTable;