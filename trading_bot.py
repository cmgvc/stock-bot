import alpaca_trade_api as tradeapi
import time
import yfinance as yf
import pandas as pd
import logging
from datetime import datetime
import pytz

# Alpaca API keys (Replace with your own)
api = tradeapi.REST('PKQRRJ8GKX59EUIBT7U0', 'Jq6NHemEEioIWV2QbVgYfnt7FnQi8PgbFWuwQrZx', base_url='https://paper-api.alpaca.markets')

# Define the list of stocks you want to trade
symbols = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD', 'SPY', 'QQQ', 
    'BABA', 'NFLX', 'DIS', 'V', 'PYPL', 'BA', 'CSCO', 'GS', 'JPM', 'WMT', 'MCD', 
    'UNH', 'CVX', 'XOM', 'GS', 'INTC', 'ORCL', 'ZM', 'SNAP', 'TWTR', 'SQ', 'PFE', 
    'MRNA', 'KO', 'PEP', 'INTU', 'LMT', 'RTX', 'BA', 'T', 'VZ', 'JNJ', 'ABT', 'NKE'
]  # Add as many stocks as you want

# Define max portfolio percentage to risk per trade (e.g., 2%)
MAX_RISK_PERCENT = 0.02  # 2% of the portfolio per trade

# Initialize logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# RSI calculation function
def rsi(data, period=14): 
    delta = data.diff().dropna() 
    gain = delta.where(delta > 0, 0) 
    loss = -delta.where(delta < 0, 0) 
    avg_gain = gain.rolling(window=period).mean() 
    avg_loss = loss.rolling(window=period).mean() 
    rs = avg_gain / avg_loss 
    return 100 - (100 / (1 + rs))

# Function to check current position for a given symbol
def check_positions(symbol): 
    positions = api.list_positions() 
    for position in positions: 
        if position.symbol == symbol: 
            return int(position.qty) 
    return 0

# Function to calculate the maximum quantity of shares to buy based on risk management
def get_max_qty(symbol, cash_balance):
    # Fetch the current price of the stock
    data = yf.download(symbol, period="1d", interval="1m")
    if data.empty:
        print(f"No data for {symbol}")
        return None  # Or return a default value or handle the error accordingly
    current_price = data['Close'].iloc[-1]
    max_amount_to_risk = cash_balance * MAX_RISK_PERCENT
    max_qty = max_amount_to_risk // current_price  # Max quantity based on cash balance
    return int(max_qty.iloc[0])  # Access the first element of the Series

# Function to place buy/sell orders based on RSI strategy
def trade(symbol, qty, cash_balance): 
    try:
        # Fetch the last 14 days of data for each symbol
        data = yf.download(symbol, period="14d", interval="1d")
        current_rsi = rsi(data['Close'], 14)[-1]  # Compute RSI based on the latest 14 days
        position_qty = check_positions(symbol)
        
        # Fetch current price
        current_price = yf.download(symbol, period="1d", interval="1m")['Close'].iloc[-1]

        # Buy order when RSI < 30 and no existing position
        if current_rsi < 30 and position_qty == 0:
            if qty > 0:  # If the risk-based quantity is valid
                api.submit_order(symbol=symbol, qty=qty, side='buy', type='market', time_in_force='gtc')
                logging.info(f"Buy order placed for {symbol} at RSI {current_rsi}, Price: {current_price}")
                print(f"Buy order placed for {symbol} at RSI {current_rsi}, Price: {current_price}")
        
        # Sell order when RSI > 70 and there is an existing position
        elif current_rsi > 70 and position_qty > 0:
            api.submit_order(symbol=symbol, qty=position_qty, side='sell', type='market', time_in_force='gtc')
            logging.info(f"Sell order placed for {symbol} at RSI {current_rsi}, Price: {current_price}")
            print(f"Sell order placed for {symbol} at RSI {current_rsi}, Price: {current_price}")
        
        # If no action is taken, it will print that it's holding
        else:
            print(f"Holding {symbol} (Current RSI: {current_rsi}, Position: {position_qty})")
    
    except Exception as e:
        logging.error(f"Error executing trade for {symbol}: {e}")
        print(f"Error executing trade for {symbol}: {e}")

# Get current cash balance from Alpaca
def get_cash_balance():
    account = api.get_account()
    return float(account.cash)

# Start trading loop for multiple symbols
def start_trading():
    while True:
        cash_balance = get_cash_balance()  # Get available cash balance
        for symbol in symbols:
            qty = get_max_qty(symbol, cash_balance)  # Calculate the max quantity to risk per trade
            if qty is not None and qty > 0:  # Check if qty is not None
                trade(symbol, qty, cash_balance)
        time.sleep(86400)  # Sleep for 1 day (86400 seconds)

# Call start_trading() to begin the trading loop
start_trading()
