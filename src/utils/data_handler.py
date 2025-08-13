"""
Data fetching and processing utilities
"""
import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from typing import Optional, Tuple


@st.cache_data
def fetch_stock_data(ticker: str, start_date, end_date) -> Optional[pd.DataFrame]:
    """
    Fetch stock data from Yahoo Finance
    
    Args:
        ticker: Stock symbol
        start_date: Start date for data
        end_date: End date for data
        
    Returns:
        DataFrame with OHLCV data or None if error
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None


def calculate_technical_indicators(data: pd.DataFrame, 
                                 show_ema: bool = True,
                                 ema_short: int = 20,
                                 ema_long: int = 50,
                                 show_rsi: bool = True,
                                 show_bollinger: bool = False,
                                 sma_short: int = 20,
                                 sma_long: int = 50) -> pd.DataFrame:
    """
    Calculate technical indicators for the given data
    
    Args:
        data: OHLCV DataFrame
        show_ema: Whether to calculate EMA
        ema_short: Short EMA period
        ema_long: Long EMA period
        show_rsi: Whether to calculate RSI
        show_bollinger: Whether to calculate Bollinger Bands
        sma_short: Short SMA period for strategy
        sma_long: Long SMA period for strategy
        
    Returns:
        DataFrame with technical indicators added
    """
    df = data.copy()
    
    # EMA
    if show_ema:
        df[f'EMA_{ema_short}'] = ta.trend.ema_indicator(df['Close'], window=ema_short)
        df[f'EMA_{ema_long}'] = ta.trend.ema_indicator(df['Close'], window=ema_long)
    
    # RSI
    if show_rsi:
        df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    
    # Bollinger Bands
    if show_bollinger:
        bb = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
        df['BB_Upper'] = bb.bollinger_hband()
        df['BB_Lower'] = bb.bollinger_lband()
        df['BB_Middle'] = bb.bollinger_mavg()
    
    # SMA for strategy
    df[f'SMA_{sma_short}'] = ta.trend.sma_indicator(df['Close'], window=sma_short)
    df[f'SMA_{sma_long}'] = ta.trend.sma_indicator(df['Close'], window=sma_long)
    
    return df


def get_stock_info(data: pd.DataFrame) -> dict:
    """
    Extract basic stock information from data
    
    Args:
        data: OHLCV DataFrame
        
    Returns:
        Dictionary with latest price, change, volume
    """
    if len(data) < 2:
        return {}
        
    latest_price = data['Close'].iloc[-1]
    price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    pct_change = (price_change / data['Close'].iloc[-2]) * 100
    volume = data['Volume'].iloc[-1]
    
    return {
        'latest_price': latest_price,
        'price_change': price_change,
        'pct_change': pct_change,
        'volume': volume
    }
