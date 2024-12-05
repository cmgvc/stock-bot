from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
from datetime import datetime, timedelta

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# In-memory storage for buy/sell history (to simulate a simple database)
buy_sell_history = {}

# Fetch stock data and RSI for a given symbol
def get_stock_data(symbol):
    try:
        data = yf.download(symbol, period="1mo", interval="1d")
        
        if data.empty:
            return None

        # Calculate RSI
        delta = data['Close'].diff().dropna()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # Extract the most recent closing price and RSI as float values
        stock_price = data['Close'].iloc[-1] if not data.empty else None
        rsi_value = rsi.iloc[-1] if not rsi.empty else None

        return {
            "symbol": symbol,
            "stock_price": float(stock_price.iloc[0]) if stock_price is not None else None,
            "rsi": float(rsi_value.iloc[0]) if rsi_value is not None else None,

            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None


import yfinance as yf

def get_stock_data_for_period(symbol, period):
    try:
        # Fetch stock data for the given period from Yahoo Finance
        data = yf.download(symbol, period=period, interval="1d")
        
        if data.empty:
            print(f"No data found for {symbol} in the period {period}.")
            return None
        
        print(f"Data fetched for {symbol}:")
        print(data)

        # Extract stock prices and dates for the entire period
        stock_prices = data['Close'].values.tolist()  # List of stock prices
        dates = [date.strftime('%Y-%m-%d') for date in data.index]  # List of dates as strings

        return {
            "symbol": symbol,
            "stock_prices": stock_prices,
            "dates": dates,
            "period": period
        }
    
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None



# Endpoint to get stock data for a given symbol and period (for graphing)
@app.route('/api/stocks/<symbol>/graph', methods=['GET'])
def get_stock_data_for_graph(symbol):
    # Get the period from query parameters (default to '1mo')
    print('hi')
    period = request.args.get('period')
    print(period)
    stock_data = get_stock_data_for_period(symbol, period)
    if stock_data:
        return jsonify(stock_data)  # Return the stock data as JSON
    else:
        return jsonify({"error": "No data for this symbol or period"}), 404

# Endpoint to get stock data
@app.route('/api/stocks/<symbol>', methods=['GET'])
def get_symbol_data(symbol):
    stock_data = get_stock_data(symbol)
    if stock_data:
        return jsonify(stock_data)  # Directly return the dictionary as JSON
    else:
        return jsonify({"error": "No data for this symbol"}), 404

# Endpoint to record a buy/sell transaction
@app.route('/api/buysell/<symbol>', methods=['POST'])
def record_transaction(symbol):
    transaction = request.json  # Get the transaction data from the request body
    
    # Ensure required fields are in the request
    if 'action' not in transaction or 'quantity' not in transaction or 'price' not in transaction:
        return jsonify({"error": "Invalid request, missing action, quantity, or price"}), 400
    
    action = transaction['action']  # Buy or sell action
    quantity = transaction['quantity']  # Number of shares
    price = transaction['price']  # Price at which the stock was bought/sold
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Timestamp of the transaction
    
    # Store the transaction in the history
    if symbol not in buy_sell_history:
        buy_sell_history[symbol] = []
    
    buy_sell_history[symbol].append({
        "action": action,
        "quantity": quantity,
        "price": price,
        "timestamp": timestamp
    })
    
    return jsonify({"message": "Transaction recorded successfully"}), 200

# Endpoint to get buy/sell history for a given symbol
@app.route('/api/buysell-history/<symbol>', methods=['GET'])
def get_buy_sell_history(symbol):
    history = buy_sell_history.get(symbol, [])
    print(history)
    return jsonify(history)

# CORS headers to allow frontend access
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # CORS header to allow frontend access
    return response

if __name__ == '__main__':
    app.run(debug=True)
