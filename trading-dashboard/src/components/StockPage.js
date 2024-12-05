import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const StockPage = ({ symbol }) => {
    const [stockData, setStockData] = useState(null);
    const [buySellHistory, setBuySellHistory] = useState([]);

    useEffect(() => {
        fetchStockData(symbol);
        fetchBuySellHistory(symbol);
    }, [symbol]);

    const fetchStockData = async (symbol) => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/api/stocks/${symbol}`);
            setStockData(response.data);
        } catch (error) {
            console.error("Error fetching stock data", error);
        }
    };

    const fetchBuySellHistory = async (symbol) => {
        try {
            const response = await axios.get(`http://127.0.0.1:5000/api/buysell-history/${symbol}`);
            setBuySellHistory(response.data);
        } catch (error) {
            console.error("Error fetching buy/sell history", error);
        }
    };

    const handleBuy = async () => {
        const price = stockData.stock_price;
        try {
            await axios.post(`http://127.0.0.1:5000/api/buysell-history/${symbol}`, {
                action: 'Buy',
                price
            });
            fetchBuySellHistory(symbol);
        } catch (error) {
            console.error("Error recording buy action", error);
        }
    };

    const handleSell = async () => {
        const price = stockData.stock_price;
        try {
            await axios.post(`http://127.0.0.1:5000/api/buysell-history/${symbol}`, {
                action: 'Sell',
                price
            });
            fetchBuySellHistory(symbol);
        } catch (error) {
            console.error("Error recording sell action", error);
        }
    };

    return (
        <div>
            <h1>{symbol} Stock Data</h1>
            {stockData ? (
                <>
                    <p>Current Price: {stockData.stock_price}</p>
                    <p>RSI: {stockData.rsi}</p>
                    <p>Date: {stockData.date}</p>

                    {/* Graph displaying stock price */}
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={stockData.priceHistory}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="date" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="price" stroke="#8884d8" />
                        </LineChart>
                    </ResponsiveContainer>

                    {/* Displaying Buy/Sell History */}
                    <h2>Buy/Sell History</h2>
                    <ul>
                        {buySellHistory.map((entry, index) => (
                            <li key={index}>
                                {entry.date}: {entry.action} at ${entry.price}
                            </li>
                        ))}
                    </ul>

                    <button onClick={handleBuy}>Buy Stock</button>
                    <button onClick={handleSell}>Sell Stock</button>
                </>
            ) : (
                <p>Loading stock data...</p>
            )}
        </div>
    );
};

export default StockPage;
