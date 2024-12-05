import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import StockTab from './components/StockTab';
import StockGraph from './components/StockGraph';
import BuySellHistory from './components/BuySellHistory';

const App = () => {
  const [stocks, setStocks] = useState(['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META']);
  const [stockData, setStockData] = useState({});
  const [buySellHistory, setBuySellHistory] = useState({});
  const [activeTab, setActiveTab] = useState('AAPL');
  const [period, setPeriod] = useState('1mo');  // Default period is 1 month
  const [graphData, setGraphData] = useState({});

  // Fetch stock data for a given symbol
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

  const fetchStockGraphData = (symbol, period) => {
    axios.get(`http://127.0.0.1:5000/api/stocks/${symbol}/graph?period=${period}`)
      .then(response => {
        setGraphData(prevData => ({
          ...prevData,
          [symbol]: response.data
        }));
      })
      .catch(error => {
        console.error("Error fetching graph data for symbol:", symbol, error);
      });
  };

  // Fetch buy/sell history
  const fetchBuySellHistory = (symbol) => {
    axios.get(`http://127.0.0.1:5000/api/buysell-history/${symbol}`)
      .then(response => {
        setBuySellHistory(prevHistory => ({
          ...prevHistory,
          [symbol]: response.data
        }));
      })
      .catch(error => {
        console.error("Error fetching buy/sell history for symbol:", symbol, error);
      });
  };

  // Fetch data when active tab or period changes
  useEffect(() => {
    fetchStockData(activeTab);
    fetchStockGraphData(activeTab, period);  // Fetch data specifically for the graph
    fetchBuySellHistory(activeTab);
  }, [activeTab, period]);  // Re-run when either activeTab or period changes

  const handlePeriodChange = (event) => {
    setPeriod(event.target.value);
  };

  return (
    <div className="App">
      <h1>Trading Dashboard</h1>

      {/* Dropdown for selecting time period */}
      <div className="period-selector">
        <select onChange={handlePeriodChange} value={period}>
          <option value="1d">1 Day</option>
          <option value="1wk">1 Week</option>
          <option value="1mo">1 Month</option>
          <option value="1y">1 Year</option>
        </select>
      </div>

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

      {/* Display stock data, graph, and history if available */}
      {stockData[activeTab] ? (
        <div>
          <StockTab symbol={activeTab} data={stockData[activeTab]} />
          <StockGraph data={graphData[activeTab]} />
          <BuySellHistory history={buySellHistory[activeTab]} />
        </div>
      ) : (
        <p>Loading data for {activeTab}...</p>
      )}
    </div>
  );
};

export default App;
