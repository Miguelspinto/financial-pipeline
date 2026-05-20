import pandas as pd
import os

# Sample stock data
data = {
    "date": ["2026-05-06", "2026-05-05", "2026-05-04", "2026-05-01"],
    "symbol": ["AAPL", "AAPL", "AAPL", "AAPL"],
    "open": [281.915, 276.925, 279.655, 278.855],
    "close": [287.51, 284.18, 276.83, 280.14],
    "volume": [58336072, 49311712, 46668401, 79915442],
    "price_change": [5.595, 7.255, -2.825, 1.285],
    "risk": ["HIGH", "HIGH", "LOW", "LOW"]
}

df = pd.DataFrame(data)

# Save as CSV
df.to_csv('stock_data.csv', index=False)

# Save as Parquet
df.to_parquet('stock_data.parquet', index=False)

# Compare file sizes
csv_size = os.path.getsize('stock_data.csv')
parquet_size = os.path.getsize('stock_data.parquet')

print(f"CSV size: {csv_size} bytes")
print(f"Parquet size: {parquet_size} bytes")
print(f"Parquet is {round(csv_size / parquet_size, 1)}x smaller")

# Read Parquet back
df_parquet = pd.read_parquet('stock_data.parquet')
print(f"\nRead back from Parquet:")
print(df_parquet)

# Show data types preserved
print(f"\nData types:")
print(df_parquet.dtypes)

# Show CSV data types for comparison
df_csv = pd.read_csv('stock_data.csv')
print(f"\nCSV data types for comparison:")
print(df_csv.dtypes)