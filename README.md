# Financial Pipeline

An automated financial data pipeline built with Python.

## What it does
- Pulls real stock data from Alpha Vantage API
- Cleans and transforms data with Pandas
- Classifies risk based on price movement
- Saves output as Parquet and CSV
- Logs all operations with timestamps

## Technologies
- Python 3.9
- Pandas
- Requests
- PyArrow

## Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Usage
python3 stock_pipeline_v2.py