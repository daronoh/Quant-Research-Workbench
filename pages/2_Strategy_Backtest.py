"""
Strategy Backtest Page - SMA Crossover and Performance Analysis
"""
import streamlit as st
import sys
from pathlib import Path

import os
import sys
from pathlib import Path

try:
    from src.utils.strategies import SMAStrategy
    from src.utils.charts import create_performance_chart
    from src.components.ui_components import render_performance_metrics
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error(f"Current working directory: {os.getcwd()}")
    st.error(f"Python path: {sys.path}")
    st.error(f"Files in current dir: {list(Path('.').glob('**/*.py'))}")
    st.stop()

st.set_page_config(page_title="Strategy Backtest", layout="wide")

def main():
    st.title("Strategy Backtesting")
    st.markdown("Test and optimize your trading strategies")
    st.markdown("---")
    
    # Check if we have data from stock analysis
    if 'data_with_indicators' not in st.session_state:
        st.warning("No stock data available. Please run stock analysis first.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Stock Analysis", use_container_width=True):
                st.switch_page("pages/1_Stock_Analysis.py")
        with col2:
            if st.button("Go to Homepage", use_container_width=True):
                st.switch_page("main.py")
        return
    
    current_ticker = st.session_state.get('current_ticker', 'Unknown')
    st.success(f"Data loaded for **{current_ticker}**")
    
    # Strategy parameters
    st.sidebar.header("Strategy Parameters")
    
    strategy_type = st.sidebar.selectbox(
        "Strategy Type",
        ["SMA Crossover", "EMA Crossover (Coming Soon)", "RSI Mean Reversion (Coming Soon)"]
    )
    
    # Initialize default values
    sma_short, sma_long, transaction_cost = 20, 50, 0.0005
    
    if strategy_type == "SMA Crossover":
        st.sidebar.subheader("SMA Parameters")
        sma_short = st.sidebar.slider("Short SMA Period", 5, 50, 20)
        sma_long = st.sidebar.slider("Long SMA Period", 20, 200, 50)
        
        # Advanced parameters
        st.sidebar.subheader("Advanced Settings")
        transaction_cost = st.sidebar.number_input("Transaction Cost (bps)", 0, 100, 5) / 10000
        min_hold_period = st.sidebar.slider("Minimum Hold Period (days)", 0, 30, 1)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"{strategy_type} Strategy")
        
        if strategy_type == "SMA Crossover":
            st.write(f"**Parameters**: SMA({sma_short}) vs SMA({sma_long}) crossover")
            st.write(f"**Transaction Cost**: {transaction_cost*10000:.1f} basis points")
            
            # Strategy description
            with st.expander("Strategy Description"):
                st.markdown("""
                **Simple Moving Average (SMA) Crossover Strategy**
                
                - **Buy Signal**: When short SMA crosses above long SMA
                - **Sell Signal**: When short SMA crosses below long SMA
                - **Logic**: Trend-following strategy that captures momentum
                
                **Pros**:
                - Simple and widely used
                - Works well in trending markets
                - Easy to understand and implement
                
                **Cons**:
                - Generates false signals in sideways markets
                - Lagging indicator (late entry/exit)
                - High transaction costs in choppy markets
                """)
        
        if st.button("Run Backtest", type="primary", use_container_width=True):
            with st.spinner("Running backtest..."):
                # Initialize strategy
                strategy = SMAStrategy(short_period=sma_short, long_period=sma_long)
                
                # Run backtest
                backtest_data, metrics = strategy.backtest(st.session_state.data_with_indicators)
                
                # Store results for metrics page
                st.session_state.backtest_results = {
                    'data': backtest_data,
                    'metrics': metrics,
                    'strategy_name': f"SMA({sma_short},{sma_long})",
                    'parameters': {
                        'sma_short': sma_short,
                        'sma_long': sma_long,
                        'transaction_cost': transaction_cost
                    }
                }
                
                # Display performance chart
                performance_fig = create_performance_chart(
                    backtest_data, 
                    f"SMA({sma_short},{sma_long}) Strategy"
                )
                st.plotly_chart(performance_fig, use_container_width=True)
                
                # Quick metrics overview
                st.subheader("Performance Summary")
                render_performance_metrics(metrics)
                
                # Trade analysis
                signals = backtest_data[backtest_data['Position'] != 0]
                if len(signals) > 0:
                    num_trades = len(signals)
                    st.metric("Number of Trades", num_trades)
                
                # Navigation
                st.success("Backtest completed! View detailed metrics on the next page.")
                if st.button("View Detailed Metrics", use_container_width=True):
                    st.switch_page("pages/3_Performance_Metrics.py")
    
    with col2:
        st.subheader("📋 Current Setup")
        
        # Display current stock info
        if 'stock_data' in st.session_state:
            stock_data = st.session_state.stock_data
            latest_price = stock_data['Close'].iloc[-1]
            st.metric("Current Stock", current_ticker)
            st.metric("Latest Price", f"${latest_price:.2f}")
            st.metric("Data Points", len(stock_data))
            
            date_range = f"{stock_data.index[0].strftime('%Y-%m-%d')} to {stock_data.index[-1].strftime('%Y-%m-%d')}"
            st.text(f"Period: {date_range}")
        
        st.markdown("---")
        
        # Quick navigation
        st.subheader("Navigation")
        if st.button("Back to Analysis", use_container_width=True):
            st.switch_page("pages/1_Stock_Analysis.py")
        if st.button("View Metrics", use_container_width=True):
            st.switch_page("pages/3_Performance_Metrics.py")
        if st.button("Homepage", use_container_width=True):
            st.switch_page("main.py")
        
        # Strategy comparison (future feature)
        st.markdown("---")
        st.subheader("Coming Soon")
        st.info("Multi-strategy comparison and optimization")

if __name__ == "__main__":
    main()
