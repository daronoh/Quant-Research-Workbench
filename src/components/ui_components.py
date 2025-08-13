"""
Reusable Streamlit UI components
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


def render_sidebar_controls() -> Dict[str, Any]:
    """
    Render sidebar controls and return all input values
    
    Returns:
        Dictionary with all control values
    """
    st.sidebar.header("Analysis Parameters")
    
    # Ticker input
    ticker = st.sidebar.text_input(
        "Enter Ticker Symbol", 
        value="AAPL", 
        help="e.g., AAPL, MSFT, GOOGL"
    )
    
    # Date range selection
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365),
            max_value=datetime.now()
        )
    with col2:
        end_date = st.date_input(
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
    
    # Strategy parameters
    st.sidebar.subheader("Strategy Parameters")
    sma_short = st.sidebar.slider("SMA Short Period", 5, 50, 20)
    sma_long = st.sidebar.slider("SMA Long Period", 20, 200, 50)
    
    # Run analysis button
    run_analysis = st.sidebar.button("Run Analysis", type="primary")
    
    return {
        'ticker': ticker,
        'start_date': start_date,
        'end_date': end_date,
        'show_ema': show_ema,
        'show_rsi': show_rsi,
        'show_bollinger': show_bollinger,
        'ema_short': ema_short,
        'ema_long': ema_long,
        'sma_short': sma_short,
        'sma_long': sma_long,
        'run_analysis': run_analysis
    }


def render_stock_info_panel(stock_info: Dict[str, Any], 
                          current_rsi: Optional[float] = None) -> None:
    """
    Render stock information panel
    
    Args:
        stock_info: Dictionary with stock metrics
        current_rsi: Current RSI value (optional)
    """
    st.subheader("Stock Info")
    
    if 'latest_price' in stock_info:
        st.metric(
            label="Latest Price",
            value=f"${stock_info['latest_price']:.2f}",
            delta=f"{stock_info['pct_change']:.2f}%"
        )
        
        st.metric(
            label="Volume",
            value=f"{stock_info['volume']:,.0f}"
        )
    
    if current_rsi is not None:
        st.metric(
            label="Current RSI",
            value=f"{current_rsi:.1f}"
        )


def render_performance_metrics(metrics: Dict[str, str]) -> None:
    """
    Render performance metrics in columns
    
    Args:
        metrics: Dictionary with performance metrics
    """
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics_list = list(metrics.items())
    
    with col1:
        if len(metrics_list) > 0:
            st.metric(metrics_list[0][0], metrics_list[0][1])
    with col2:
        if len(metrics_list) > 1:
            st.metric(metrics_list[1][0], metrics_list[1][1])
    with col3:
        if len(metrics_list) > 2:
            st.metric(metrics_list[2][0], metrics_list[2][1])
    with col4:
        if len(metrics_list) > 3:
            st.metric(metrics_list[3][0], metrics_list[3][1])
    with col5:
        if len(metrics_list) > 4:
            st.metric(metrics_list[4][0], metrics_list[4][1])


def render_welcome_screen() -> None:
    """Render the welcome screen when no analysis is running"""
    st.info("Enter a ticker symbol and click 'Run Analysis' to get started!")
    
    st.subheader("What You'll Get:")
    st.markdown("""
    - **Interactive Price Charts**: Candlestick charts with volume
    - **Technical Indicators**: EMA, RSI, Bollinger Bands
    - **Strategy Backtesting**: SMA crossover with performance metrics
    - **Real-time Data**: Live data from Yahoo Finance
    """)
    
    st.subheader("Popular Tickers to Try:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Tech Stocks:**")
        st.markdown("- AAPL (Apple)")
        st.markdown("- MSFT (Microsoft)")
        st.markdown("- GOOGL (Google)")
        
    with col2:
        st.markdown("**ETFs:**")
        st.markdown("- SPY (S&P 500)")
        st.markdown("- QQQ (Nasdaq)")
        st.markdown("- VTI (Total Market)")
        
    with col3:
        st.markdown("**Crypto:**")
        st.markdown("- BTC-USD (Bitcoin)")
        st.markdown("- ETH-USD (Ethereum)")
        st.markdown("- DOGE-USD (Dogecoin)")
