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

# Never hardcode API keys in real projects — for now it's fine locally
API_KEY = "I0GBED553DQT5RVT"
SYMBOL = "AAPL"

url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}"

logger.info(f"Fetching data for {SYMBOL}")

response = requests.get(url)
data = response.json()

logger.info(f"Status code: {response.status_code}")
logger.info(f"Keys in response: {list(data.keys())}")
logger.info(f"First key: {list(data.keys())[0]}")
logger.info(f"Second key: {list(data.keys())[1]}")


# Extract the time series data
time_series = data['Time Series (Daily)']

# Convert to DataFrame
df = pd.DataFrame(time_series).T

# T means transpose — flips rows and columns
# Each date becomes a row instead of a column

logger.info(f"DataFrame shape: {df.shape}")
logger.info(f"Columns: {list(df.columns)}")
logger.info(f"First 5 rows:\n{df.head()}")


# Rename columns to cleaner names
df.columns = ['open', 'high', 'low', 'close', 'volume']

# Convert all values to numbers — they came in as strings
df = df.astype(float)

# Add the date as a proper column instead of index
df.index.name = 'date'
df = df.reset_index()

# Add a daily price change column
df['price_change'] = df['close'] - df['open']

# Add a risk flag
df['risk'] = df['price_change'].apply(
    lambda x: "HIGH" if abs(x) > 5 else "LOW"
)

logger.info(f"Cleaned DataFrame:\n{df.head()}")
logger.info(f"HIGH risk days: {len(df[df['risk'] == 'HIGH'])}")

df.to_csv('aapl_stock_data.csv', index=False)
logger.info("Data saved to aapl_stock_data.csv")

