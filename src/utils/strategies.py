"""
Trading strategies and backtesting utilities
"""
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any


class SMAStrategy:
    """Simple Moving Average Crossover Strategy"""
    
    def __init__(self, short_period: int = 20, long_period: int = 50):
        self.short_period = short_period
        self.long_period = long_period
        
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on SMA crossover
        
        Args:
            data: DataFrame with price data and SMA columns
            
        Returns:
            DataFrame with signals added
        """
        df = data.copy()
        
        # Calculate SMAs if not present
        sma_short_col = f'SMA_{self.short_period}'
        sma_long_col = f'SMA_{self.long_period}'
        
        if sma_short_col not in df.columns:
            df[sma_short_col] = df['Close'].rolling(window=self.short_period).mean()
        if sma_long_col not in df.columns:
            df[sma_long_col] = df['Close'].rolling(window=self.long_period).mean()
        
        # Generate signals
        df['Signal'] = 0
        df.loc[df[sma_short_col] > df[sma_long_col], 'Signal'] = 1
        df.loc[df[sma_short_col] < df[sma_long_col], 'Signal'] = -1
        
        # Create position column (1 for long, 0 for neutral, -1 for short)
        df['Position'] = df['Signal'].shift(1)  # Use previous signal for position
        df['Position'] = df['Position'].fillna(0)
        
        return df
    
    def backtest(self, data: pd.DataFrame, transaction_cost: float = 0.001) -> Tuple[pd.DataFrame, Dict[str, str]]:
        """
        Run complete backtest for the strategy
        
        Args:
            data: DataFrame with OHLCV and indicator data
            transaction_cost: Transaction cost as a fraction (e.g., 0.001 = 0.1%)
            
        Returns:
            Tuple of (backtest_data, performance_metrics)
        """
        df = self.generate_signals(data)
        
        # Calculate returns
        df['Returns'] = df['Close'].pct_change()
        
        # Calculate strategy returns with transaction costs
        df['Strategy_Returns'] = df['Position'] * df['Returns']
        
        # Apply transaction costs when position changes
        position_changes = df['Position'].diff().abs()
        df['Transaction_Costs'] = position_changes * transaction_cost
        df['Strategy_Returns'] = df['Strategy_Returns'] - df['Transaction_Costs']
        
        # Calculate cumulative returns
        df['Cumulative_Returns'] = (1 + df['Returns']).cumprod()
        df['Cumulative_Strategy'] = (1 + df['Strategy_Returns']).cumprod()
        
        # Calculate performance metrics
        metrics = self.calculate_metrics(df)
        
        return df, metrics
    
    def calculate_metrics(self, df: pd.DataFrame) -> Dict[str, str]:
        """Calculate performance metrics"""
        total_return = df['Cumulative_Strategy'].iloc[-1] - 1
        annual_return = (df['Cumulative_Strategy'].iloc[-1] ** (252 / len(df))) - 1
        volatility = df['Strategy_Returns'].std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility > 0 else 0
        max_drawdown = (df['Cumulative_Strategy'] / df['Cumulative_Strategy'].cummax() - 1).min()
        
        return {
            'Total Return': f"{total_return:.2%}",
            'Annual Return (CAGR)': f"{annual_return:.2%}",
            'Volatility': f"{volatility:.2%}",
            'Sharpe Ratio': f"{sharpe_ratio:.2f}",
            'Max Drawdown': f"{max_drawdown:.2%}"
        }


def calculate_additional_metrics(strategy_returns: pd.Series) -> Dict[str, float]:
    """
    Calculate additional risk metrics
    
    Args:
        strategy_returns: Series of strategy returns
        
    Returns:
        Dictionary with additional metrics
    """
    # Remove NaN values
    returns = strategy_returns.dropna()
    
    if len(returns) == 0:
        return {}
    
    # Additional metrics
    win_rate = (returns > 0).sum() / len(returns)
    best_day = returns.max()
    worst_day = returns.min()
    
    # Calmar ratio (CAGR / Max Drawdown)
    cumulative = (1 + returns).cumprod()
    max_dd = (cumulative / cumulative.cummax() - 1).min()
    annual_return = (cumulative.iloc[-1] ** (252 / len(returns))) - 1
    calmar_ratio = annual_return / abs(max_dd) if max_dd != 0 else 0
    
    return {
        'win_rate': win_rate,
        'best_day': best_day,
        'worst_day': worst_day,
        'calmar_ratio': calmar_ratio
    }
