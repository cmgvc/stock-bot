import alpaca_trade_api as tradeapi
import time
import yfinance as yf

# Initialize Alpaca API
api = tradeapi.REST('PKQRRJ8GKX59EUIBT7U0', 'Jq6NHemEEioIWV2QbVgYfnt7FnQi8PgbFWuwQrZx', base_url='https://paper-api.alpaca.markets')

# Fetch RSI calculation
def rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# Function to check available cash in the account
def check_cash():
    account = api.get_account()
    print(f"Available Cash: ${account.cash}")

# Function to check current positions
def check_positions():
    positions = api.list_positions()
    if positions:
        for position in positions:
            print(f"Position in {position.symbol}: {position.qty} shares")
    else:
        print("No current positions.")

# Function to fetch current stock price
# Function to get the current price of a symbol
def get_current_price(symbol):
    try:
        current_price = api.get_latest_trade(symbol).price  # Use get_latest_trade instead of get_last_trade
        print(f"Current price of {symbol}: ${current_price}")
        return current_price
    except Exception as e:
        print(f"Error fetching current price for {symbol}: {e}")
        return None


# Function to place a buy order if RSI < 30
def place_buy_order(symbol, qty):
    # Get historical data for RSI calculation
    data = yf.download(symbol, period="1mo", interval="1d")
    data['RSI'] = rsi(data['Close'])

    # Get the latest RSI value
    current_rsi = data['RSI'].iloc[-1]
    print(f"Current RSI for {symbol}: {current_rsi}")

    if current_rsi < 30:
        print(f"RSI is below 30, placing buy order for {qty} shares of {symbol}")
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"Buy order placed for {symbol}")
    else:
        print(f"RSI is not below 30, no buy order placed for {symbol}")

# Main trading loop (only one cycle for trial)
symbol = 'SPY'  # You can replace this with any stock you want to trade
qty = 1  # Number of shares to buy
print("Starting trial run...")

# Check cash and positions before placing a trade
check_cash()
check_positions()
get_current_price(symbol)

# Place buy order if conditions are met
place_buy_order(symbol, qty)

# End the trial run after 1 cycle
print("Trial run complete.")
