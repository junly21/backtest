"""
Application constants
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Data Sources
YAHOO_FINANCE_BASE_URL = "https://finance.yahoo.com/quote"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)

# ETF Tickers
ETF_TICKERS = ["SPY", "QQQ", "GLD", "TIP", "BIL"]

# Database
PRICE_TABLE_NAME = "etf_prices"

# Batch Settings
BATCH_TIME = os.getenv("BATCH_TIME", "18:00")  # EST 기준 18시 

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "backtest")
DB_USER = os.getenv("DB_USER", "backtest")
DB_PASSWORD = os.getenv("DB_PASSWORD", "backtest")

# Database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
