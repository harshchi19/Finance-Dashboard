import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def algo_strag():

    def set_background(image_url):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url({image_url});
                background-size: fit;
                background-position: center;
                background-repeat: repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    set_background("https://img.freepik.com/free-vector/seamless-white-interlaced-rounded-arc-patterned-background_53876-97975.jpg")
    st.markdown("""
        <style>
            html{
                font-family: Manrope;
                }
            .e1nzilvr2{
                text-align:center;
                text-shadow: 0px 2px 5.3px rgba(0, 0, 0, 0.19);
                font-family: Manrope;
                font-size: 72px;
                font-style: normal;
                font-weight: 600;
                line-height: 83px; 
                letter-spacing: -2.16px;
                opacity: 0;
                animation: fadeIn 2s forwards;
                }
             .ea3mdgi5{
                max-width:100%;
                }
    </style>
        """, unsafe_allow_html=True)

    st.title('Algorithm Comparison')

    # Fetch data function
    def fetch_data(ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            st.warning("No data found for the ticker and date range.")
        else:
            st.write(f"Data fetched for {ticker} from {start_date} to {end_date}")
        return data

    # Define strategies
    def sma_crossover_strategy(data, short_window=40, long_window=100):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
        signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
        signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()
        return signals

    def rsi_strategy(data, window=14):
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = np.where(rsi < 30, 1.0, np.where(rsi > 70, -1.0, 0.0))
        signals['positions'] = signals['signal'].diff()
        return signals

    def bollinger_bands_strategy(data, window=20):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        rolling_mean = data['Close'].rolling(window).mean()
        rolling_std = data['Close'].rolling(window).std()
        signals['upper_band'] = rolling_mean + (rolling_std * 2)
        signals['lower_band'] = rolling_mean - (rolling_std * 2)
        signals['signal'] = np.where(data['Close'] < signals['lower_band'], 1.0, 0.0)
        signals['signal'] = np.where(data['Close'] > signals['upper_band'], -1.0, signals['signal'])
        signals['positions'] = signals['signal'].diff()
        return signals

    def macd_strategy(data, short_window=12, long_window=26, signal_window=9):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0
        short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
        long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
        signals['macd'] = short_ema - long_ema
        signals['macd_signal'] = signals['macd'].ewm(span=signal_window, adjust=False).mean()
        signals['signal'] = np.where(signals['macd'] > signals['macd_signal'], 1.0, -1.0)
        signals['positions'] = signals['signal'].diff()
        return signals

    def buy_and_hold(data):
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 1.0  # Always hold the stock
        signals['positions'] = signals['signal'].diff()
        return signals

    def calculate_returns(data, signals):
        returns = pd.DataFrame(index=data.index)
        returns['daily_returns'] = data['Close'].pct_change()
        returns['strategy_returns'] = returns['daily_returns'] * signals['positions'].shift()
        returns['cumulative_returns'] = (1 + returns['strategy_returns']).cumprod()
        return returns

    # User input
    st.sidebar.header('User Input Parameters')
    ticker = st.sidebar.text_input('Ticker Symbol', 'AAPL')
    start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-01-01'))

    if st.button("Run Comparison"):
        data = fetch_data(ticker, start_date, end_date)
        
        if data.empty:
            st.error("No data available for the selected ticker and date range.")
        else:
            strategies = {
                "SMA Crossover": sma_crossover_strategy(data),
                "RSI": rsi_strategy(data),
                "MACD": macd_strategy(data),
                "Buy and Hold": buy_and_hold(data)
            }
            
            returns = {}
            for name, signals in strategies.items():
                returns[name] = calculate_returns(data, signals)['cumulative_returns']
            
            returns_df = pd.DataFrame(returns)
            
            # Calculate performance metrics
            total_returns = returns_df.iloc[-1] - 1
            annualized_returns = (1 + total_returns) ** (252 / len(returns_df)) - 1
            sharpe_ratios = np.sqrt(252) * returns_df.pct_change().mean() / returns_df.pct_change().std()
            max_drawdowns = (returns_df / returns_df.cummax() - 1).min()
            
            metrics = pd.DataFrame({
                "Total Return": total_returns,
                "Annualized Return": annualized_returns,
                "Sharpe Ratio": sharpe_ratios,
                "Max Drawdown": max_drawdowns
            })
            
            # Display results
            st.subheader("Strategy Performance Metrics")
            st.dataframe(metrics.style.format("{:.2%}"))
            
            # Plot cumulative returns
            fig, ax = plt.subplots(figsize=(12, 6))
            for name, returns in returns_df.items():
                ax.plot(returns.index, returns, label=name)
            ax.set_title(f'Cumulative Returns Comparison - {ticker}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Cumulative Returns')
            ax.legend()
            st.pyplot(fig)
            
            # Display raw data
            st.subheader("Raw Data (First Few Rows)")
            st.write(returns_df.head())

            # Conclusion
            st.subheader("Conclusion")
            
            best_strategy = metrics['Total Return'].idxmax()
            worst_strategy = metrics['Total Return'].idxmin()
            
            best_return = metrics.loc[best_strategy, 'Total Return']
            best_sharpe = metrics.loc[best_strategy, 'Sharpe Ratio']
            best_drawdown = metrics.loc[best_strategy, 'Max Drawdown']
            
            st.write(f"Based on the analysis, the best performing strategy for {ticker} over the given period was the *{best_strategy}* strategy.")
            st.write(f"It achieved a total return of {best_return:.2%}, with a Sharpe ratio of {best_sharpe:.2f} and a maximum drawdown of {best_drawdown:.2%}.")
            
            if best_strategy != "Buy and Hold":
                buy_hold_return = metrics.loc["Buy and Hold", 'Total Return']
                outperformance = best_return - buy_hold_return
                st.write(f"This strategy outperformed the simple Buy and Hold approach by {outperformance:.2%}.")
            
            st.write(f"\nThe worst performing strategy was the *{worst_strategy}* strategy.")
            
            # Additional insights
            if best_strategy == "SMA Crossover":
                st.write("\nThe success of the SMA Crossover strategy suggests that the stock had clear trending periods where the shorter-term average consistently outperformed the longer-term average.")
            elif best_strategy == "RSI":
                st.write("\nThe RSI strategy's success indicates that the stock had frequent overbought and oversold conditions that quickly reversed.")
            elif best_strategy == "Bollinger Bands":
                st.write("\nThe Bollinger Bands strategy performed well, suggesting that the stock had consistent price reversals at the upper and lower bands.")
            elif best_strategy == "MACD":
                st.write("\nThe MACD strategy's performance indicates that the stock had strong trends that were well-captured by the convergence and divergence of the moving averages.")
            elif best_strategy == "Buy and Hold":
                st.write("\nThe Buy and Hold strategy outperformed all active strategies, suggesting that the stock had a strong overall upward trend with limited opportunities for successful market timing.")
            
            st.write("\nIt's important to note that past performance doesn't guarantee future results. The best strategy can vary depending on the specific stock and market conditions. Always consider risk management and diversification in real-world trading applications.")

if __name__ == "__main__":
    algo_strag()
