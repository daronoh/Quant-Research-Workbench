"""
Stock Analysis Page - Interactive Charts and Technical Indicators
"""
import streamlit as st
import os
from pathlib import Path
from datetime import datetime, timedelta

try:
    from src.utils.data_handler import fetch_stock_data, calculate_technical_indicators, get_stock_info
    from src.utils.charts import create_price_chart
    from src.components.ui_components import render_stock_info_panel
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error(f"Current working directory: {os.getcwd()}")
    st.error(f"Files in current dir: {list(Path('.').glob('**/*.py'))}")
    st.stop()

st.set_page_config(page_title="Stock Analysis", layout="wide")

def main():
    st.title("Stock Analysis")
    st.markdown("Interactive price charts with technical indicators")
    st.markdown("---")
    
    # Sidebar controls
    st.sidebar.header("Analysis Parameters")
    
    # Use selected ticker from homepage if available
    default_ticker = st.session_state.get('selected_ticker', 'AAPL')
    ticker = st.sidebar.text_input("Enter Ticker Symbol", value=default_ticker, help="e.g., AAPL, MSFT, GOOGL")
    
    # Date range selection
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.sidebar.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365),
            max_value=datetime.now()
        )
    with col2:
        end_date = st.sidebar.date_input(
            "End Date", 
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    # Technical indicators toggles
    st.sidebar.subheader("Technical Indicators")
    show_ema = st.sidebar.checkbox("Show EMA", value=True)
    show_rsi = st.sidebar.checkbox("Show RSI", value=True)
    show_bollinger = st.sidebar.checkbox("Show Bollinger Bands", value=False)
    
    # EMA parameters
    ema_short, ema_long = 20, 50
    if show_ema:
        ema_short = st.sidebar.slider("EMA Short Period", 5, 50, 20)
        ema_long = st.sidebar.slider("EMA Long Period", 20, 200, 50)
    
    # Run analysis button
    run_analysis = st.sidebar.button("Run Analysis", type="primary")
    
    if run_analysis and ticker:
        with st.spinner(f"Fetching data for {ticker}..."):
            # Fetch data
            stock_data = fetch_stock_data(ticker, start_date, end_date)
            
            if stock_data is not None and not stock_data.empty:
                # Store data in session state for other pages
                st.session_state.stock_data = stock_data
                st.session_state.current_ticker = ticker
                
                # Calculate indicators
                data_with_indicators = calculate_technical_indicators(
                    stock_data,
                    show_ema=show_ema,
                    ema_short=ema_short,
                    ema_long=ema_long,
                    show_rsi=show_rsi,
                    show_bollinger=show_bollinger,
                    sma_short=20,  # Default for strategy
                    sma_long=50
                )
                st.session_state.data_with_indicators = data_with_indicators
                st.session_state.analysis_params = {
                    'show_ema': show_ema,
                    'ema_short': ema_short,
                    'ema_long': ema_long,
                    'show_rsi': show_rsi,
                    'show_bollinger': show_bollinger
                }
                
                # Create layout
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Display price chart
                    chart = create_price_chart(
                        data_with_indicators,
                        ticker,
                        show_ema=show_ema,
                        ema_short=ema_short,
                        ema_long=ema_long,
                        show_rsi=show_rsi,
                        show_bollinger=show_bollinger
                    )
                    st.plotly_chart(chart, use_container_width=True)
                
                with col2:
                    # Display stock info
                    stock_info = get_stock_info(stock_data)
                    current_rsi = None
                    if show_rsi and 'RSI' in data_with_indicators.columns:
                        current_rsi = data_with_indicators['RSI'].iloc[-1]
                    
                    render_stock_info_panel(stock_info, current_rsi)
                    
                    # Navigation to other pages
                    st.markdown("---")
                    st.subheader("Next Steps")
                    if st.button("Run Strategy Backtest", use_container_width=True):
                        st.switch_page("2_Strategy_Backtest")
                    if st.button("View Performance Metrics", use_container_width=True):
                        st.switch_page("3_Performance_Metrics")
            
            else:
                st.error("Unable to fetch data. Please check the ticker symbol and try again.")
    
    else:
        st.info("Enter a ticker symbol and click 'Run Analysis' to get started!")
        
        # Show popular tickers
        st.subheader("Popular Stocks")
        col1, col2, col3, col4 = st.columns(4)
        
        popular_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "META", "NFLX"]
        
        for i, ticker_option in enumerate(popular_tickers):
            col = [col1, col2, col3, col4][i % 4]
            with col:
                if st.button(f"{ticker_option}", key=f"quick_{ticker_option}"):
                    st.session_state.selected_ticker = ticker_option
                    st.rerun()

if __name__ == "__main__":
    main()
