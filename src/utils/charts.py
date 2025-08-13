"""
Chart creation and visualization utilities
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_price_chart(data: pd.DataFrame, 
                      ticker: str,
                      show_ema: bool = True,
                      ema_short: int = 20,
                      ema_long: int = 50,
                      show_rsi: bool = True,
                      show_bollinger: bool = False) -> go.Figure:
    """
    Create comprehensive price chart with technical indicators
    
    Args:
        data: DataFrame with OHLCV and indicator data
        ticker: Stock symbol for title
        show_ema: Whether to show EMA lines
        ema_short: Short EMA period
        ema_long: Long EMA period
        show_rsi: Whether to show RSI panel
        show_bollinger: Whether to show Bollinger Bands
        
    Returns:
        Plotly figure object
    """
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
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
    
    # EMA indicators
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
        
        # RSI overbought/oversold lines - add as scatter traces instead of hlines
        fig.add_trace(
            go.Scatter(
                x=[data.index[0], data.index[-1]],
                y=[70, 70],
                mode='lines',
                name='RSI Overbought (70)',
                line=dict(color='red', dash='dash', width=1),
                opacity=0.5,
                showlegend=False
            ),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=[data.index[0], data.index[-1]],
                y=[30, 30],
                mode='lines',
                name='RSI Oversold (30)',
                line=dict(color='green', dash='dash', width=1),
                opacity=0.5,
                showlegend=False
            ),
            row=3, col=1
        )
    
    fig.update_layout(
        title=f"{ticker} Price Analysis",
        xaxis_title="Date",
        height=800,
        showlegend=True,
        template="plotly_white"
    )
    
    fig.update_xaxes(rangeslider_visible=False)
    
    return fig


def create_performance_chart(backtest_data: pd.DataFrame, 
                           strategy_name: str = "SMA Strategy") -> go.Figure:
    """
    Create strategy performance comparison chart
    
    Args:
        backtest_data: DataFrame with cumulative returns
        strategy_name: Name of the strategy for legend
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=backtest_data.index,
            y=backtest_data['Cumulative_Returns'],
            mode='lines',
            name='Buy & Hold',
            line=dict(color='blue', width=2)
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=backtest_data.index,
            y=backtest_data['Cumulative_Strategy'],
            mode='lines',
            name=strategy_name,
            line=dict(color='red', width=2)
        )
    )
    
    fig.update_layout(
        title="Strategy Performance Comparison",
        xaxis_title="Date",
        yaxis_title="Cumulative Returns",
        template="plotly_white",
        height=500
    )
    
    return fig
