import alpaca_trade_api as tradeapi
import pandas as pd
import time
from datetime import datetime, timedelta

API_KEY = ''
SECRET_KEY = ''
BASE_URL = 'https://paper-api.alpaca.markets'  # Use paper trading URL for testing

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)

SYMBOL = 'AAPL'
QTY = 1
LOOKBACK_DAYS = 100  # Fetch historical data for the past year
Z_SCORE_THRESHOLD = 1.0

def calculate_z_score(symbol):
    try:
        end = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        start = (datetime.now() - timedelta(days=LOOKBACK_DAYS)).strftime('%Y-%m-%d')

        barset = api.get_bars(symbol, '1D', start=start, end=end)

        if barset:
            closes = closes = pd.Series([bar.c for bar in barset])
            
            print("Closes:", len(closes))
            
            if len(closes) > 0:
                mean = closes.mean()
                std_dev = closes.std()
                current_price = closes.iloc[-1]

                z_score = (current_price - mean) / std_dev

                print("Mean:", mean)
                print("Standard Deviation:", std_dev)
                print("Current Price:", current_price)
                print("Z-Score:", z_score)

                return z_score
            else:
                return None
        else:
            print("No barset data available.")
            return None
    except Exception as e:
        print(f"Error occurred while calculating z-score: {str(e)}")
        return None

def mean_reversion_strategy():
    z_score = calculate_z_score(SYMBOL)

    if z_score is not None:
        if z_score > Z_SCORE_THRESHOLD:
            print("Selling opportunity detected. Selling AAPL.")
            api.submit_order(
                symbol=SYMBOL,
                qty=QTY,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
        elif z_score < -Z_SCORE_THRESHOLD:
            print("Buying opportunity detected. Buying AAPL.")
            api.submit_order(
                symbol=SYMBOL,
                qty=QTY,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
        else:
            print("No trading opportunity detected.")
    else:
        print("Unable to calculate z-score. Skipping trading.")

if __name__ == "__main__":
    while True:
        mean_reversion_strategy()
        print("Waiting for next trading cycle...")
        time.sleep(60)  # Run once every minute
