"""
Quant Research Workbench - Main Homepage
"""
import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Quant Research Workbench",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main homepage"""
    
    # Title and description
    st.title("Quant Research Workbench")
    st.markdown("**Interactive Equity Analysis Dashboard**")
    st.markdown("---")
    
    # Welcome section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## Welcome to Your Quantitative Research Platform
        
        This dashboard provides comprehensive tools for equity analysis, technical indicators, 
        and strategy backtesting. Navigate using the sidebar to access different modules.
        
        ### Current Features:
        - **Stock Analysis**: Interactive price charts with technical indicators
        - **Strategy Backtesting**: SMA crossover with performance metrics
        - **Real-time Data**: Live data from Yahoo Finance
        
        ### Coming Soon (Phase 2):
        - **Factor Research**: Momentum, mean reversion, volume analysis
        - **Portfolio Analytics**: Multi-asset risk and attribution
        - **Options Analytics**: Greeks, volatility surfaces
        """)
        
        # Quick stats or featured content
        st.subheader("Quick Start")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("Analyze Stocks", use_container_width=True):
                st.switch_page("pages/Stock_Analysis.py")
        with col_b:
            if st.button("Run Backtests", use_container_width=True):
                st.switch_page("pages/Strategy_Backtest.py")
        with col_c:
            if st.button("View Metrics", use_container_width=True):
                st.switch_page("pages/Performance_Metrics.py")
    
    with col2:
        st.subheader("Popular Tickers")
        
        # Popular tickers with quick access
        tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA"]
        
        for ticker in tickers:
            if st.button(f"{ticker}", key=f"ticker_{ticker}", use_container_width=True):
                # Store selected ticker in session state
                st.session_state.selected_ticker = ticker
                st.switch_page("pages/Stock_Analysis.py")
        
        st.markdown("---")
        
        # ETFs and indices
        st.subheader("ETFs & Indices")
        etfs = ["SPY", "QQQ", "IWM", "VTI"]
        
        for etf in etfs:
            if st.button(f"{etf}", key=f"etf_{etf}", use_container_width=True):
                st.session_state.selected_ticker = etf
                st.switch_page("pages/Stock_Analysis.py")

if __name__ == "__main__":
    main()
