import React from 'react';

const StockTab = ({ symbol, data }) => {
  console.log('StockTab received props:', { symbol, data });

  if (!data) return <div>No data available for {symbol}</div>;

  return (
    <div>
      <h2>{symbol}</h2>
      <p>Price: {data.stock_price.toFixed(2)}</p>
      <p>RSI: {data.rsi.toFixed(3)}</p>
    </div>
  );
};


export default StockTab;
