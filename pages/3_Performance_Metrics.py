"""
Performance Metrics Page - Detailed Strategy Analysis and Risk Metrics
"""
import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import os

try:
    from src.utils.strategies import calculate_additional_metrics
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error(f"Current working directory: {os.getcwd()}")
    st.error(f"Files in current dir: {list(Path('.').glob('**/*.py'))}")
    st.stop()

st.set_page_config(page_title="Performance Metrics", layout="wide")

def create_drawdown_chart(backtest_data):
    """Create drawdown chart"""
    cumulative = backtest_data['Cumulative_Strategy']
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=backtest_data.index,
        y=drawdown * 100,
        fill='tonexty',
        name='Drawdown %',
        line=dict(color='red', width=1)
    ))
    
    fig.update_layout(
        title="Strategy Drawdown Over Time",
        xaxis_title="Date",
        yaxis_title="Drawdown (%)",
        template="plotly_white",
        height=400
    )
    
    return fig

def create_returns_distribution(backtest_data):
    """Create returns distribution histogram"""
    returns = backtest_data['Strategy_Returns'].dropna() * 100
    
    fig = px.histogram(
        x=returns,
        nbins=50,
        title="Daily Returns Distribution",
        labels={'x': 'Daily Returns (%)', 'y': 'Frequency'}
    )
    
    # Add vertical lines for mean and std
    mean_return = returns.mean()
    std_return = returns.std()
    
    fig.add_vline(x=mean_return, line_dash="dash", line_color="green", 
                  annotation_text=f"Mean: {mean_return:.2f}%")
    fig.add_vline(x=mean_return + std_return, line_dash="dash", line_color="orange",
                  annotation_text=f"+1σ: {mean_return + std_return:.2f}%")
    fig.add_vline(x=mean_return - std_return, line_dash="dash", line_color="orange",
                  annotation_text=f"-1σ: {mean_return - std_return:.2f}%")
    
    fig.update_layout(template="plotly_white", height=400)
    
    return fig

def main():
    st.title("Performance Metrics")
    st.markdown("Detailed strategy analysis and risk metrics")
    st.markdown("---")
    
    # Check if we have backtest results
    if 'backtest_results' not in st.session_state:
        st.warning("No backtest results available. Please run a strategy backtest first.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Go to Strategy Backtest", use_container_width=True):
                st.switch_page("pages/2_Strategy_Backtest.py")
        with col2:
            if st.button("Go to Homepage", use_container_width=True):
                st.switch_page("main.py")
        return
    
    results = st.session_state.backtest_results
    backtest_data = results['data']
    metrics = results['metrics']
    strategy_name = results['strategy_name']
    
    st.success(f"Analysis for **{strategy_name}** Strategy")
    
    # Performance overview
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
    
    # Detailed analysis
    tab1, tab2, tab3, tab4 = st.tabs(["Performance", "Risk Analysis", "Trade Analysis", "Raw Data"])
    
    with tab1:
        st.subheader("Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Cumulative returns chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=backtest_data.index,
                y=backtest_data['Cumulative_Returns'],
                mode='lines',
                name='Buy & Hold',
                line=dict(color='blue', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=backtest_data.index,
                y=backtest_data['Cumulative_Strategy'],
                mode='lines',
                name=strategy_name,
                line=dict(color='red', width=2)
            ))
            
            fig.update_layout(
                title="Cumulative Returns Comparison",
                xaxis_title="Date",
                yaxis_title="Cumulative Returns",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Rolling returns
            window = 30
            rolling_strategy = backtest_data['Strategy_Returns'].rolling(window).sum()
            rolling_benchmark = backtest_data['Returns'].rolling(window).sum()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=backtest_data.index,
                y=rolling_benchmark * 100,
                mode='lines',
                name=f'{window}D Buy & Hold',
                line=dict(color='blue', width=1)
            ))
            
            fig.add_trace(go.Scatter(
                x=backtest_data.index,
                y=rolling_strategy * 100,
                mode='lines',
                name=f'{window}D {strategy_name}',
                line=dict(color='red', width=1)
            ))
            
            fig.update_layout(
                title=f"{window}-Day Rolling Returns",
                xaxis_title="Date",
                yaxis_title="Rolling Returns (%)",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Risk Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Drawdown chart
            drawdown_fig = create_drawdown_chart(backtest_data)
            st.plotly_chart(drawdown_fig, use_container_width=True)
        
        with col2:
            # Returns distribution
            dist_fig = create_returns_distribution(backtest_data)
            st.plotly_chart(dist_fig, use_container_width=True)
        
        # Additional risk metrics
        st.subheader("Additional Risk Metrics")
        
        try:
            additional_metrics = calculate_additional_metrics(backtest_data['Strategy_Returns'])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Win Rate", f"{additional_metrics.get('win_rate', 0):.1%}")
            with col2:
                st.metric("Best Day", f"{additional_metrics.get('best_day', 0):.2%}")
            with col3:
                st.metric("Worst Day", f"{additional_metrics.get('worst_day', 0):.2%}")
            with col4:
                st.metric("Calmar Ratio", f"{additional_metrics.get('calmar_ratio', 0):.2f}")
                
        except Exception as e:
            st.warning(f"Could not calculate additional metrics: {e}")
    
    with tab3:
        st.subheader("Trade Analysis")
        
        # Extract trades
        signals = backtest_data[backtest_data['Position'] != 0].copy()
        
        if len(signals) > 0:
            # Trade statistics
            buys = signals[signals['Position'] > 0]
            sells = signals[signals['Position'] < 0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Trades", len(signals))
            with col2:
                st.metric("Buy Signals", len(buys))
            with col3:
                st.metric("Sell Signals", len(sells))
            
            # Show recent trades
            st.subheader("Recent Trade Signals")
            
            trade_display = signals[['Close', 'Signal', 'Position']].tail(10)
            trade_display['Action'] = trade_display['Position'].apply(
                lambda x: 'BUY' if x > 0 else 'SELL'
            )
            trade_display['Price'] = trade_display['Close'].apply(lambda x: f"${x:.2f}")
            
            st.dataframe(
                trade_display[['Price', 'Action']].rename(columns={'Price': 'Trade Price'}),
                use_container_width=True
            )
            
        else:
            st.info("No trade signals generated for this strategy and time period.")
    
    with tab4:
        st.subheader("Raw Data")
        
        # Data export options
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write("Download the complete backtest dataset:")
        
        with col2:
            csv = backtest_data.to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{strategy_name}_backtest_results.csv",
                mime="text/csv"
            )
        
        # Show data preview
        st.subheader("Data Preview")
        
        display_columns = ['Close', 'Signal', 'Returns', 'Strategy_Returns', 
                          'Cumulative_Returns', 'Cumulative_Strategy']
        available_columns = [col for col in display_columns if col in backtest_data.columns]
        
        st.dataframe(
            backtest_data[available_columns].tail(50),
            use_container_width=True
        )
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Back to Analysis", use_container_width=True):
            st.switch_page("pages/1_Stock_Analysis.py")
    with col2:
        if st.button("New Backtest", use_container_width=True):
            st.switch_page("pages/2_Strategy_Backtest.py")
    with col3:
        if st.button("Homepage", use_container_width=True):
            st.switch_page("main.py")

if __name__ == "__main__":
    main()
