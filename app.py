from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

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
            "stock_price": float(stock_price) if stock_price is not None else None,
            "rsi": float(rsi_value) if rsi_value is not None else None,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

@app.route('/api/stocks/<symbol>', methods=['GET'])
def get_symbol_data(symbol):
    stock_data = get_stock_data(symbol)
    if stock_data:
        return jsonify(stock_data)  # Directly return the dictionary as JSON
    else:
        return jsonify({"error": "No data for this symbol"}), 404
    

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # CORS header to allow frontend access
    return response

if __name__ == '__main__':
    app.run(debug=True)
