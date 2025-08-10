import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ta
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Quant Research Workbench",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📊 Quant Research Workbench")
st.markdown("**Interactive Multi-Asset Research Dashboard**")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("📈 Analysis Parameters")

# Ticker input
ticker = st.sidebar.text_input("Enter Ticker Symbol", value="AAPL", help="e.g., AAPL, MSFT, GOOGL")

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
st.sidebar.subheader("📊 Technical Indicators")
show_ema = st.sidebar.checkbox("Show EMA", value=True)
show_rsi = st.sidebar.checkbox("Show RSI", value=True)
show_bollinger = st.sidebar.checkbox("Show Bollinger Bands", value=False)

# EMA parameters
if show_ema:
    ema_short = st.sidebar.slider("EMA Short Period", 5, 50, 20)
    ema_long = st.sidebar.slider("EMA Long Period", 20, 200, 50)

# Strategy parameters
st.sidebar.subheader("⚙️ Strategy Parameters")
sma_short = st.sidebar.slider("SMA Short Period", 5, 50, 20)
sma_long = st.sidebar.slider("SMA Long Period", 20, 200, 50)

# Run analysis button
run_analysis = st.sidebar.button("🚀 Run Analysis", type="primary")

@st.cache_data
def fetch_data(ticker, start, end):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start, end=end)
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def calculate_technical_indicators(data):
    """Calculate technical indicators"""
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

def create_price_chart(data):
    """Create candlestick chart with volume"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Price & Indicators', 'Volume', 'RSI'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=f'{ticker} Price'
        ),
        row=1, col=1
    )
    
    # Technical indicators
    if show_ema and f'EMA_{ema_short}' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[f'EMA_{ema_short}'],
                mode='lines',
                name=f'EMA {ema_short}',
                line=dict(color='orange', width=2)
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data[f'EMA_{ema_long}'],
                mode='lines',
                name=f'EMA {ema_long}',
                line=dict(color='red', width=2)
            ),
            row=1, col=1
        )
    
    # Bollinger Bands
    if show_bollinger and 'BB_Upper' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['BB_Upper'],
                mode='lines',
                name='BB Upper',
                line=dict(color='gray', dash='dash'),
                opacity=0.5
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['BB_Lower'],
                mode='lines',
                name='BB Lower',
                line=dict(color='gray', dash='dash'),
                fill='tonexty',
                opacity=0.3
            ),
            row=1, col=1
        )
    
    # Volume
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume',
            marker_color='lightblue',
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # RSI
    if show_rsi and 'RSI' in data.columns:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data['RSI'],
                mode='lines',
                name='RSI',
                line=dict(color='purple', width=2)
            ),
            row=3, col=1
        )
        
        # RSI overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)
    
    fig.update_layout(
        title=f"{ticker} Price Analysis",
        xaxis_title="Date",
        height=800,
        showlegend=True,
        template="plotly_white"
    )
    
    fig.update_xaxes(rangeslider_visible=False)
    
    return fig

def simple_sma_backtest(data):
    """Simple SMA crossover backtest"""
    df = data.copy()
    
    # Generate signals
    df['Signal'] = 0
    df['Signal'][df[f'SMA_{sma_short}'] > df[f'SMA_{sma_long}']] = 1
    df['Position'] = df['Signal'].diff()
    
    # Calculate returns
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Signal'].shift(1) * df['Returns']
    
    # Calculate cumulative returns
    df['Cumulative_Returns'] = (1 + df['Returns']).cumprod()
    df['Cumulative_Strategy'] = (1 + df['Strategy_Returns']).cumprod()
    
    # Performance metrics
    total_return = df['Cumulative_Strategy'].iloc[-1] - 1
    annual_return = (df['Cumulative_Strategy'].iloc[-1] ** (252 / len(df))) - 1
    volatility = df['Strategy_Returns'].std() * np.sqrt(252)
    sharpe_ratio = annual_return / volatility if volatility > 0 else 0
    max_drawdown = (df['Cumulative_Strategy'] / df['Cumulative_Strategy'].cummax() - 1).min()
    
    return df, {
        'Total Return': f"{total_return:.2%}",
        'Annual Return (CAGR)': f"{annual_return:.2%}",
        'Volatility': f"{volatility:.2%}",
        'Sharpe Ratio': f"{sharpe_ratio:.2f}",
        'Max Drawdown': f"{max_drawdown:.2%}"
    }

# Main application logic
if run_analysis and ticker:
    with st.spinner(f"Fetching data for {ticker}..."):
        # Fetch data
        stock_data = fetch_data(ticker, start_date, end_date)
        
        if stock_data is not None and not stock_data.empty:
            # Calculate indicators
            data_with_indicators = calculate_technical_indicators(stock_data)
            
            # Create two columns for layout
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Display price chart
                chart = create_price_chart(data_with_indicators)
                st.plotly_chart(chart, use_container_width=True)
            
            with col2:
                # Display basic info
                st.subheader("📊 Stock Info")
                latest_price = stock_data['Close'].iloc[-1]
                price_change = stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]
                pct_change = (price_change / stock_data['Close'].iloc[-2]) * 100
                
                st.metric(
                    label="Latest Price",
                    value=f"${latest_price:.2f}",
                    delta=f"{pct_change:.2f}%"
                )
                
                st.metric(
                    label="Volume",
                    value=f"{stock_data['Volume'].iloc[-1]:,.0f}"
                )
                
                if show_rsi and 'RSI' in data_with_indicators.columns:
                    current_rsi = data_with_indicators['RSI'].iloc[-1]
                    st.metric(
                        label="Current RSI",
                        value=f"{current_rsi:.1f}"
                    )
            
            # Backtest section
            st.subheader("⚙️ SMA Crossover Strategy Backtest")
            
            if st.button("Run Backtest"):
                backtest_data, metrics = simple_sma_backtest(data_with_indicators)
                
                # Display metrics
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("Total Return", metrics['Total Return'])
                with col2:
                    st.metric("CAGR", metrics['Annual Return (CAGR)'])
                with col3:
                    st.metric("Sharpe Ratio", metrics['Sharpe Ratio'])
                with col4:
                    st.metric("Volatility", metrics['Volatility'])
                with col5:
                    st.metric("Max Drawdown", metrics['Max Drawdown'])
                
                # Plot performance comparison
                performance_fig = go.Figure()
                
                performance_fig.add_trace(
                    go.Scatter(
                        x=backtest_data.index,
                        y=backtest_data['Cumulative_Returns'],
                        mode='lines',
                        name='Buy & Hold',
                        line=dict(color='blue')
                    )
                )
                
                performance_fig.add_trace(
                    go.Scatter(
                        x=backtest_data.index,
                        y=backtest_data['Cumulative_Strategy'],
                        mode='lines',
                        name='SMA Strategy',
                        line=dict(color='red')
                    )
                )
                
                performance_fig.update_layout(
                    title="Strategy Performance Comparison",
                    xaxis_title="Date",
                    yaxis_title="Cumulative Returns",
                    template="plotly_white"
                )
                
                st.plotly_chart(performance_fig, use_container_width=True)
        
        else:
            st.error("Unable to fetch data. Please check the ticker symbol and try again.")

else:
    st.info("👈 Enter a ticker symbol and click 'Run Analysis' to get started!")
    
    # Show sample data
    st.subheader("🎯 What You'll Get:")
    st.markdown("""
    - **📈 Interactive Price Charts**: Candlestick charts with volume
    - **📊 Technical Indicators**: EMA, RSI, Bollinger Bands
    - **⚙️ Strategy Backtesting**: SMA crossover with performance metrics
    - **📱 Real-time Data**: Live data from Yahoo Finance
    """)
