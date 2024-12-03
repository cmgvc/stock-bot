import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Stock Tab Component
const StockTab = ({ symbol, data }) => {
  return (
    <div className="stock-tab">
      <h2>{symbol}</h2>
      <p>Stock Price: ${data.stock_price}</p>
      <p>RSI: {data.rsi}</p>
      <p>Last Updated: {data.date}</p>
    </div>
  );
};

// App Component
const App = () => {
  const [stocks, setStocks] = useState([
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META'
  ]);
  const [stockData, setStockData] = useState({});
  const [activeTab, setActiveTab] = useState('AAPL');

  // Fetch stock data from the Flask backend
  const fetchStockData = (symbol) => {
    axios.get(`http://127.0.0.1:5000/api/stocks/${symbol}`)
      .then(response => {
        setStockData(prevData => ({
          ...prevData,
          [symbol]: response.data
        }));
      })
      .catch(error => {
        console.error("Error fetching data for symbol:", symbol, error);
      });
  };

  useEffect(() => {
    // Initially fetch data for the active tab
    fetchStockData(activeTab);
  }, [activeTab]);

  return (
    <div className="App">
      <h1>Trading Dashboard</h1>
      
      {/* Tabs for switching between stock symbols */}
      <div className="tabs">
        {stocks.map(symbol => (
          <button 
            key={symbol} 
            className={`tab-button ${symbol === activeTab ? 'active' : ''}`}
            onClick={() => setActiveTab(symbol)}
          >
            {symbol}
          </button>
        ))}
      </div>

      {/* Display the stock data */}
      {stockData[activeTab] ? (
        <StockTab symbol={activeTab} data={stockData[activeTab]} />
      ) : (
        <p>Loading data for {activeTab}...</p>
      )}
    </div>
  );
};

export default App;
