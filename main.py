"""
Quant Research Workbench - Main Application
"""
import streamlit as st
import sys
import os
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from src.utils.data_handler import fetch_stock_data, calculate_technical_indicators, get_stock_info
    from src.utils.charts import create_price_chart, create_performance_chart
    from src.utils.strategies import SMAStrategy
    from src.components.ui_components import (
        render_sidebar_controls, 
        render_stock_info_panel, 
        render_performance_metrics,
        render_welcome_screen
    )
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please make sure all modules are in the correct directories.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Quant Research Workbench",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("Quant Research Workbench")
st.markdown("**Interactive Equity Analysis Dashboard**")
st.markdown("---")

# Initialize session state
if 'show_backtest' not in st.session_state:
    st.session_state.show_backtest = False

def main():
    """Main application logic"""
    
    # Render sidebar controls
    controls = render_sidebar_controls()
    
    # Main analysis logic
    if controls['run_analysis'] and controls['ticker']:
        st.session_state.show_backtest = True
        
        with st.spinner(f"Fetching data for {controls['ticker']}..."):
            # Fetch data
            stock_data = fetch_stock_data(
                controls['ticker'], 
                controls['start_date'], 
                controls['end_date']
            )
            
            if stock_data is not None and not stock_data.empty:
                # Store data in session state
                st.session_state.stock_data = stock_data
                st.session_state.controls = controls
                
                # Calculate indicators
                data_with_indicators = calculate_technical_indicators(
                    stock_data,
                    show_ema=controls['show_ema'],
                    ema_short=controls['ema_short'],
                    ema_long=controls['ema_long'],
                    show_rsi=controls['show_rsi'],
                    show_bollinger=controls['show_bollinger'],
                    sma_short=controls['sma_short'],
                    sma_long=controls['sma_long']
                )
                st.session_state.data_with_indicators = data_with_indicators
                
                # Create layout
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Display price chart
                    chart = create_price_chart(
                        data_with_indicators,
                        controls['ticker'],
                        show_ema=controls['show_ema'],
                        ema_short=controls['ema_short'],
                        ema_long=controls['ema_long'],
                        show_rsi=controls['show_rsi'],
                        show_bollinger=controls['show_bollinger']
                    )
                    st.plotly_chart(chart, use_container_width=True)
                
                with col2:
                    # Display stock info
                    stock_info = get_stock_info(stock_data)
                    current_rsi = None
                    if controls['show_rsi'] and 'RSI' in data_with_indicators.columns:
                        current_rsi = data_with_indicators['RSI'].iloc[-1]
                    
                    render_stock_info_panel(stock_info, current_rsi)
            
            else:
                st.error("Unable to fetch data. Please check the ticker symbol and try again.")
                st.session_state.show_backtest = False
    
    # Backtest section
    if st.session_state.show_backtest and 'data_with_indicators' in st.session_state:
        st.subheader("SMA Crossover Strategy Backtest")
        
        # Get current SMA parameters from stored controls
        stored_controls = st.session_state.get('controls', {})
        sma_short = stored_controls.get('sma_short', 20)
        sma_long = stored_controls.get('sma_long', 50)
        
        st.write(f"**Strategy**: SMA({sma_short}) vs SMA({sma_long}) crossover")
        
        if st.button("Run Backtest", key="backtest_button"):
            with st.spinner("Running backtest..."):
                # Initialize strategy
                strategy = SMAStrategy(short_period=sma_short, long_period=sma_long)
                
                # Run backtest
                backtest_data, metrics = strategy.backtest(st.session_state.data_with_indicators)
                
                # Display metrics
                render_performance_metrics(metrics)
                
                # Display performance chart
                performance_fig = create_performance_chart(
                    backtest_data, 
                    f"SMA({sma_short},{sma_long}) Strategy"
                )
                st.plotly_chart(performance_fig, use_container_width=True)
    
    elif not st.session_state.show_backtest:
        render_welcome_screen()


if __name__ == "__main__":
    main()
