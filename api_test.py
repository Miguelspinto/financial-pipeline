import requests
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This is a free public API — no key needed
url = "https://api.frankfurter.app/latest?from=USD&to=EUR,GBP,JPY"

logger.info("Calling API...")

response = requests.get(url)

logger.info(f"Status code: {response.status_code}")
logger.info(f"Raw response: {response.text}")

import json

# Convert raw text to Python dictionary
data = response.json()
logger.info(f"Base currency: {data['base']}")
logger.info(f"Date: {data['date']}")
logger.info(f"USD to EUR: {data['rates']['EUR']}")
logger.info(f"USD to GBP: {data['rates']['GBP']}")
logger.info(f"USD to JPY: {data['rates']['JPY']}")


df = pd.DataFrame([data['rates']])

print(df)
