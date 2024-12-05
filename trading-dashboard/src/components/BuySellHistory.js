import React from 'react';

const BuySellHistory = ({ history }) => {

  return (
    <div className="buy-sell-history">
      <h3>Buy/Sell History</h3>
      <ul>
        {history && history.map((entry, index) => (
          <li key={index} style={{ color: entry.action === 'Buy' ? 'green' : 'red' }}>
            {entry.date}: {entry.action} at ${entry.price}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BuySellHistory;
