# Quant Research Workbench
**Interactive Equity Analysis Dashboard**

A Streamlit-powered quantitative research platform for single-asset equity analysis, technical indicators, and strategy backtesting. Built for quants, by quants.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)

## Current Features

### Core Equity Analysis & Backtesting
- **Interactive Price Charts**: Candlestick visualization with volume overlay
- **Technical Indicators**: EMA (configurable periods), RSI (14-period), Bollinger Bands (20-period)
- **Real-time Metrics**: Latest price, daily change, volume, current RSI
- **Strategy Backtesting**: SMA crossover with configurable short/long periods
- **Performance Metrics**: Total Return, CAGR, Sharpe Ratio, Volatility, Maximum Drawdown
- **Data Source**: Yahoo Finance API with automatic caching

## Project Roadmap

### Phase 1: Core Equities Research & Backtesting
- [x] Basic charting infrastructure
- [x] Technical indicators
- [x] Simple backtesting framework
- [x] Yahoo Finance integration

### Phase 2: Factor Research Module
- [ ] Factor calculation engine
- [ ] IC analysis framework
- [ ] Factor PnL simulation
- [ ] Rolling performance metrics

### Phase 3: Portfolio Risk & Attribution
- [ ] Multi-asset portfolio support
- [ ] Risk metrics calculation
- [ ] Benchmark comparison
- [ ] Sector analysis

### Phase 4: Options Analytics
- [ ] Options data integration
- [ ] Greeks calculation
- [ ] IV surface modeling
- [ ] Black-Scholes implementation

### Phase 5: Advanced Backtesting Sandbox
- [ ] Strategy library expansion
- [ ] Transaction cost modeling
- [ ] Multi-strategy comparison
- [ ] Parameter optimization

### Phase 6: Deployment & Polish
- [ ] Multipage layout
- [ ] Custom theming
- [ ] Performance optimization
- [ ] Production deployment

## Technology Stack

- **Frontend**: Streamlit 1.28+
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (candlestick charts, line plots)
- **Financial Data**: yfinance (Yahoo Finance API)
- **Technical Analysis**: TA-Lib library (ta)
- **Deployment**: Local development server

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
```bash
# Clone the repository
git clone https://github.com/daronoh/Quant-Research-Workbench.git
cd Quant-Research-Workbench

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

1. **Launch the Dashboard**:
   ```bash
   .\run_app.bat
   ```

2. **Analyze Any Stock**:
   - Enter a ticker symbol (e.g., AAPL, MSFT, GOOGL, TSLA)
   - Select your preferred date range
   - Toggle technical indicators on/off
   - Adjust EMA periods with sliders

3. **Run Strategy Backtest**:
   - Configure SMA short/long periods
   - Click "Run Backtest" to see performance
   - Compare strategy vs buy-and-hold returns

## Dashboard Layout

### Sidebar Controls
- **Ticker Input**: Enter any valid stock symbol
- **Date Range**: Start and end date selectors  
- **Technical Indicators**: Toggle EMA, RSI, Bollinger Bands
- **Strategy Parameters**: Configurable SMA periods (5-200 days)

### Main Display
- **Price Chart**: 3-panel layout with price, volume, and RSI
- **Stock Metrics**: Real-time price, change %, volume, current RSI
- **Backtest Results**: Performance metrics and strategy comparison chart

## Available Indicators

### EMA (Exponential Moving Average)
- Configurable short period: 5-50 days (default: 20)
- Configurable long period: 20-200 days (default: 50)
- Visual overlay on price chart

### RSI (Relative Strength Index)
- Fixed 14-period calculation
- Overbought line at 70 (red dashed)
- Oversold line at 30 (green dashed)
- Separate panel below volume

### Bollinger Bands
- 20-period moving average
- 2 standard deviation bands
- Gray dashed lines with fill between bands

## SMA Crossover Strategy

The implemented strategy uses Simple Moving Average crossover signals:

```python
# Signal Generation
df['Signal'] = 0
df['Signal'][df[f'SMA_{short}'] > df[f'SMA_{long}']] = 1

# Performance Calculation  
df['Strategy_Returns'] = df['Signal'].shift(1) * df['Returns']
df['Cumulative_Strategy'] = (1 + df['Strategy_Returns']).cumprod()
```

### Performance Metrics
- **Total Return**: Cumulative strategy return
- **CAGR**: Compound Annual Growth Rate
- **Sharpe Ratio**: Risk-adjusted return (annualized)
- **Volatility**: Annualized standard deviation
- **Max Drawdown**: Largest peak-to-trough decline

## Data & Caching

### Data Source
- **Yahoo Finance**: Free, reliable financial data via yfinance
- **Supported Assets**: Stocks, ETFs, indices (e.g., SPY, QQQ, ^GSPC)
- **Data Range**: Historical data available for most assets

### Caching Strategy
- **Streamlit Cache**: `@st.cache_data` decorator for data fetching
- **Session Persistence**: Settings maintained during browser session
- **Automatic Refresh**: Data refetched when parameters change

## Usage Examples

### Popular Tickers to Try
- **Tech Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA
- **Market ETFs**: SPY, QQQ, IWM, VTI
- **Crypto**: BTC-USD, ETH-USD
- **Commodities**: GLD, SLV, USO

### Recommended Settings
- **Short-term Analysis**: 3-6 months, EMA(12,26), SMA(10,30)
- **Long-term Analysis**: 2-5 years, EMA(20,50), SMA(50,200)
- **Volatile Assets**: Enable Bollinger Bands for range identification
