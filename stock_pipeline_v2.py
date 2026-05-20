import requests
import pandas as pd
import logging

# Logging setup
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_pipeline.log', mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

API_KEY = "I0GBED553DQT5RVT"

def fetch_stock_data(symbol):
    logger.info(f"Fetching data for {symbol}")
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    
    # Step 1 — make the request safely
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        logger.error(f"Network error: {e}")
        return None
    
    # Step 2 — check status code
    if response.status_code != 200:
        logger.error(f"Bad status code: {response.status_code}")
        return None
    
    # Step 3 — parse JSON safely
    try:
        data = response.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        return None
    
    # Step 4 — check expected keys exist
    if 'Time Series (Daily)' not in data:
        logger.error(f"Unexpected response structure: {list(data.keys())}")
        return None
    
    # Step 5 — extract and build DataFrame
    time_series = data['Time Series (Daily)']
    df = pd.DataFrame(time_series).T
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df = df.astype(float)
    df.index.name = 'date'
    df = df.reset_index()
    df['symbol'] = symbol
    df['price_change'] = df['close'] - df['open']
    df['risk'] = df['price_change'].apply(
        lambda x: "HIGH" if abs(x) > 5 else "LOW"
    )
    
    logger.info(f"Successfully fetched {len(df)} rows for {symbol}")
    return df

# Test with multiple stocks
symbols = ['AAPL', 'MSFT', 'INVALID']

for symbol in symbols:
    df = fetch_stock_data(symbol)
    if df is not None:
        logger.info(f"{symbol} — HIGH risk days: {len(df[df['risk'] == 'HIGH'])}")
        df.to_csv(f'{symbol}_data.csv', index=False)
        logger.info(f"Saved {symbol}_data.csv")
    else:
        logger.warning(f"Skipping {symbol} — no data returned")