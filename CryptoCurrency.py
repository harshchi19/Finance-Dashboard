import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from collections import defaultdict
import requests
import json
import yfinance as yf
from web3 import Web3
from statsmodels.tsa.arima.model import ARIMA
import ccxt
from web3 import Web3

# Page layout
def crypto():
# Title
    st.title('Cryptocurrency')

    # About
    expander_bar = st.expander("About")
    expander_bar.markdown("""
    * **Instructions:** Use the top navigation to switch between different features.
    * **Features:** Price data, Advanced Analysis, Wallet simulation, Trading simulation, Stablecoin tracker, Polygon Integration, Community
    * **Data sources:** CoinMarketCap API, Yahoo Finance, Polygon Network, Simulated trading data, User-generated content
    """)

    # Top Navigation
    st.markdown("""
    <style>
    .stButton button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        price_data = st.button('Price Data')
    with col2:
        advanced_analysis = st.button('Advanced Analysis')
    with col3:
        wallet = st.button('Wallet')
    with col4:
        trading = st.button('Trading')
    with col5:
        stablecoin_tracker = st.button('Stablecoin Tracker')
    with col6:
        community = st.button('Community')

    # Initialize session state for navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'Price Data'

    # Update page based on button clicks
    if price_data:
        st.session_state.page = 'Price Data'
    elif advanced_analysis:
        st.session_state.page = 'Advanced Analysis'
    elif wallet:
        st.session_state.page = 'Wallet'
    elif trading:
        st.session_state.page = 'Trading'
    elif stablecoin_tracker:
        st.session_state.page = 'Stablecoin Tracker'
    elif community:
        st.session_state.page = 'Community'

    # Load data function (cached)
    @st.cache_data
    def load_data():
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
        'start':'1',
        'limit':'100',
        'convert':'USD'
        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '65d05907-f108-4f0c-8abb-ac90904cf30e',
        }

        try:
            response = requests.get(url, params=parameters, headers=headers)
            data = json.loads(response.text)
            df = pd.json_normalize(data['data'])
            return df
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return pd.DataFrame()

    df = load_data()

    # Get sorted coin list
    sorted_coin = sorted(df['symbol']) if not df.empty else []

    # Wallet simulation
    class Wallet:
        def __init__(self):
            self.balance = defaultdict(float)
            self.transactions = []

        def deposit(self, currency, amount):
            self.balance[currency] += amount
            self.transactions.append({
                'type': 'Deposit',
                'currency': currency,
                'amount': amount,
                'timestamp': datetime.now()
            })

        def withdraw(self, currency, amount):
            if self.balance[currency] >= amount:
                self.balance[currency] -= amount
                self.transactions.append({
                    'type': 'Withdrawal',
                    'currency': currency,
                    'amount': amount,
                    'timestamp': datetime.now()
                })
                return True
            return False

        def get_balance(self, currency):
            return self.balance[currency]

        def get_transactions(self):
            return self.transactions

    # Initialize wallet
    if 'wallet' not in st.session_state:
        st.session_state.wallet = Wallet()

    # Initialize community posts
    if 'community_posts' not in st.session_state:
        st.session_state.community_posts = []

    # Page content based on navigation
    if st.session_state.page == 'Price Data':
        st.header('Cryptocurrency Price Data')
        
        # Currency selection
        selected_coin = st.multiselect('Select Cryptocurrencies', sorted_coin, sorted_coin[:5] if len(sorted_coin) >= 5 else sorted_coin)
        df_selected_coin = df[df['symbol'].isin(selected_coin)] if not df.empty else pd.DataFrame()

        # Display data
        if not df_selected_coin.empty:
            st.dataframe(df_selected_coin)

            # Download CSV
            csv = df_selected_coin.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="crypto_data.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)

            # Advanced Price Chart
            st.subheader('Advanced Price Chart')
            selected_coin_for_chart = st.selectbox('Select a coin for detailed chart', selected_coin)
            chart_data = yf.download(f"{selected_coin_for_chart}-USD", start="2020-01-01", end=datetime.now().strftime('%Y-%m-%d'))
            
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'), row_width=[0.2, 0.7])
            
            fig.add_trace(go.Candlestick(x=chart_data.index, open=chart_data['Open'], high=chart_data['High'], low=chart_data['Low'], close=chart_data['Close'], name="OHLC"), row=1, col=1)
            fig.add_trace(go.Bar(x=chart_data.index, y=chart_data['Volume'], name="Volume"), row=2, col=1)
            
            fig.update_layout(height=600, width=800, title_text=f"{selected_coin_for_chart} Price Chart")
            fig.update_xaxes(rangeslider_visible=False, rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ))
            st.plotly_chart(fig)
        else:
            st.write("No data available.")

    elif st.session_state.page == 'Advanced Analysis':
        st.header('Advanced Cryptocurrency Analysis')

        # Correlation Heatmap
        st.subheader('Correlation Heatmap')
        if not df.empty:
            numeric_df = df.select_dtypes(include=[np.number])
            corr = numeric_df.corr()
            fig = px.imshow(corr, x=corr.columns, y=corr.columns, color_continuous_scale='RdBu_r', aspect="auto")
            fig.update_layout(title='Correlation Heatmap of Cryptocurrency Metrics', width=800, height=800)
            st.plotly_chart(fig)
        else:
            st.write("No data available for analysis.")

        # Market Dominance Pie Chart
        st.subheader('Market Dominance')
        if not df.empty:
            market_cap_data = df.nlargest(10, 'quote.USD.market_cap')[['name', 'quote.USD.market_cap']]
            fig = px.pie(market_cap_data, values='quote.USD.market_cap', names='name', title='Top 10 Cryptocurrencies by Market Cap')
            st.plotly_chart(fig)
        else:
            st.write("No data available for market dominance analysis.")

        # Price Prediction with Machine Learning
        st.subheader('Advanced Price Prediction')
        selected_coin_for_prediction = st.selectbox('Select a coin for price prediction', sorted_coin)
        days_for_prediction = st.slider('Number of days for prediction', 1, 90, 30)

        if not df.empty and selected_coin_for_prediction in df['symbol'].values:
            coin_data = yf.download(f"{selected_coin_for_prediction}-USD", start="2020-01-01", end=datetime.now().strftime('%Y-%m-%d'))
            model = ARIMA(coin_data['Close'], order=(1,1,1))
            results = model.fit()
            
            forecast = results.forecast(steps=days_for_prediction)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=coin_data.index, y=coin_data['Close'], mode='lines', name='Historical Data'))
            fig.add_trace(go.Scatter(x=pd.date_range(start=coin_data.index[-1], periods=days_for_prediction+1)[1:], y=forecast, mode='lines', name='Forecast'))
            fig.update_layout(title=f'{selected_coin_for_prediction} Price Forecast', xaxis_title='Date', yaxis_title='Price (USD)')
            st.plotly_chart(fig)
            
            st.write(f"Predicted price after {days_for_prediction} days: ${forecast[-1]:.2f}")
        else:
            st.write("No data available for prediction.")

    elif st.session_state.page == 'Wallet':
        st.header('Cryptocurrency Wallet')

        # Display current balance
        st.subheader('Current Balance')
        for currency, amount in st.session_state.wallet.balance.items():
            st.write(f"{currency}: {amount:.2f}")

        # Deposit form
        st.subheader('Deposit')
        deposit_currency = st.selectbox('Select currency to deposit', sorted_coin)
        deposit_amount = st.number_input('Enter amount to deposit', min_value=0.0, step=0.1)
        if st.button('Deposit'):
            st.session_state.wallet.deposit(deposit_currency, deposit_amount)
            st.success(f"Deposited {deposit_amount} {deposit_currency}")

        # Withdrawal form
        st.subheader('Withdraw')
        withdraw_currency = st.selectbox('Select currency to withdraw', sorted_coin)
        withdraw_amount = st.number_input('Enter amount to withdraw', min_value=0.0, step=0.1)
        if st.button('Withdraw'):
            if st.session_state.wallet.withdraw(withdraw_currency, withdraw_amount):
                st.success(f"Withdrawn {withdraw_amount} {withdraw_currency}")
            else:
                st.error("Insufficient balance")

        # Transaction history
        st.subheader('Transaction History')
        transactions = st.session_state.wallet.get_transactions()
        if transactions:
            df_transactions = pd.DataFrame(transactions)
            st.dataframe(df_transactions)
        else:
            st.write("No transactions yet")

    elif st.session_state.page == 'Trading':
        st.header('Trading Simulation')

        # Select cryptocurrency for trading
        trade_coin = st.selectbox('Select cryptocurrency to trade', sorted_coin)
        
        if not df.empty and trade_coin in df['symbol'].values:
            # Get current price
            current_price = df[df['symbol'] == trade_coin]['quote.USD.price'].iloc[0]
            st.write(f"Current price of {trade_coin}: ${current_price:.2f}")

            # Buy form
            st.subheader('Buy')
            buy_amount = st.number_input('Enter amount to buy (in USD)', min_value=0.0, step=1.0)
            if st.button('Buy'):
                coins_bought = buy_amount / current_price
                if st.session_state.wallet.withdraw('USD', buy_amount):
                    st.session_state.wallet.deposit(trade_coin, coins_bought)
                    st.success(f"Bought {coins_bought:.6f} {trade_coin}")
                else:
                    st.error("Insufficient USD balance")

            # Sell form
            st.subheader('Sell')
            max_sell = st.session_state.wallet.get_balance(trade_coin)
            sell_amount = st.number_input(f'Enter amount to sell (max {max_sell:.6f})', min_value=0.0, max_value=max_sell, step=0.000001)
            if st.button('Sell'):
                if st.session_state.wallet.withdraw(trade_coin, sell_amount):
                    usd_received = sell_amount * current_price
                    st.session_state.wallet.deposit('USD', usd_received)
                    st.success(f"Sold {sell_amount:.6f} {trade_coin} for ${usd_received:.2f}")
                else:
                    st.error(f"Insufficient {trade_coin} balance")

            # Display current portfolio
            st.subheader('Current Portfolio')
            for currency, amount in st.session_state.wallet.balance.items():
                if amount > 0:
                    if currency == 'USD':
                        st.write(f"{currency}: ${amount:.2f}")
                    else:
                        currency_price = df[df['symbol'] == currency]['quote.USD.price'].iloc[0]
                        usd_value = amount * currency_price
                        st.write(f"{currency}: {amount:.6f} (${usd_value:.2f})")

            # Portfolio performance chart (simulated)
            st.subheader('Portfolio Performance')
            dates = pd.date_range(start='1/1/2023', periods=100)
            performance = [1000]  # Starting with $1000
            for _ in range(99):
                change = np.random.normal(0, 0.02)  # Random daily change
                performance.append(performance[-1] * (1 + change))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=performance, mode='lines', name='Portfolio Value'))
            fig.update_layout(title='Simulated Portfolio Performance', xaxis_title='Date', yaxis_title='Portfolio Value ($)')
            st.plotly_chart(fig)
        else:
            st.write("No data available for trading simulation.")

    elif st.session_state.page == 'Stablecoin Tracker':
        st.header('Stablecoin Tracker')
        
        stablecoins = ['USDT', 'USDC', 'BUSD', 'DAI', 'TUSD']
        stablecoin_data = df[df['symbol'].isin(stablecoins)] if not df.empty else pd.DataFrame()
        
        if not stablecoin_data.empty:
            # Stablecoin Overview
            st.subheader('Stablecoin Overview')
            st.dataframe(stablecoin_data[['name', 'symbol', 'quote.USD.price', 'quote.USD.market_cap', 'quote.USD.volume_24h']])
            
            # Stablecoin Price Stability Chart
            st.subheader('Stablecoin Price Stability')
            fig = go.Figure()
            for coin in stablecoins:
                if coin in stablecoin_data['symbol'].values:
                    price = stablecoin_data[stablecoin_data['symbol'] == coin]['quote.USD.price'].iloc[0]
                    fig.add_trace(go.Bar(x=[coin], y=[abs(1 - price)], name=coin))
            fig.update_layout(title='Deviation from $1 Peg', yaxis_title='Absolute Deviation')
            st.plotly_chart(fig)
            
            # Stablecoin Market Share
            st.subheader('Stablecoin Market Share')
            fig = px.pie(stablecoin_data, values='quote.USD.market_cap', names='symbol', title='Stablecoin Market Share')
            st.plotly_chart(fig)
            
        else:
            st.write("No stablecoin data available.")

    if 'community_posts' not in st.session_state:
        st.session_state.community_posts = [
            {
                'title': "Bitcoin's Recent Price Surge",
                'content': "Bitcoin has seen a significant price increase over the past week. What do you think is driving this surge? Could it be institutional adoption or other factors?",
                'timestamp': datetime.now() - timedelta(days=5),
                'upvotes': 15,
                'comments': ["I think it's due to the upcoming halving event!", "Institutional investors are definitely playing a role."]
            },
            {
                'title': "Ethereum 2.0 and Its Impact on DeFi",
                'content': "With Ethereum 2.0 on the horizon, how do you think it will affect the current DeFi ecosystem? Will it solve the scalability issues?",
                'timestamp': datetime.now() - timedelta(days=3),
                'upvotes': 22,
                'comments': ["It should definitely help with gas fees!", "I'm worried about potential security issues during the transition."]
            },
            {
                'title': "Regulatory Challenges in Crypto",
                'content': "As governments worldwide are starting to pay more attention to cryptocurrencies, what regulatory challenges do you foresee? How might this affect the market?",
                'timestamp': datetime.now() - timedelta(days=2),
                'upvotes': 18,
                'comments': ["Clear regulations could actually help adoption.", "I'm concerned about privacy coins being targeted."]
            },
            {
                'title': "NFTs: Future of Digital Ownership or Bubble?",
                'content': "NFTs have exploded in popularity recently. Are they the future of digital ownership and copyright, or just a passing trend? What are your thoughts?",
                'timestamp': datetime.now() - timedelta(days=1),
                'upvotes': 30,
                'comments': ["I think they have real potential beyond just digital art.", "The environmental impact is concerning."]
            },
            {
                'title': "Stablecoins and Their Role in Crypto Markets",
                'content': "Stablecoins are playing an increasingly important role in crypto markets. How do you see their usage evolving? Are they essential for mass adoption?",
                'timestamp': datetime.now() - timedelta(hours=12),
                'upvotes': 25,
                'comments': ["They're crucial for reducing volatility.", "I worry about the backing of some stablecoins."]
            }
        ]
    elif st.session_state.page == 'Community':
        st.header('Crypto Community')

        # Post creation
        st.subheader('Create a Post')
        post_title = st.text_input('Post Title')
        post_content = st.text_area('Post Content')
        if st.button('Submit Post'):
            if post_title and post_content:
                st.session_state.community_posts.append({
                    'title': post_title,
                    'content': post_content,
                    'timestamp': datetime.now(),
                    'upvotes': 0,
                    'comments': []
                })
                st.success('Post submitted successfully!')
            else:
                st.error('Please provide both title and content for your post.')

        # Display posts
        st.subheader('Recent Posts')
        for idx, post in enumerate(reversed(st.session_state.community_posts)):
            st.write(f"**{post['title']}**")
            st.write(f"Posted on: {post['timestamp']}")
            st.write(post['content'])
            
            # Upvote button
            if st.button(f"Upvote ({post['upvotes']})", key=f"upvote_{idx}"):
                post['upvotes'] += 1
            
            # Comment section
            st.write("Comments:")
            for comment in post['comments']:
                st.write(f"- {comment}")
            
            # Add comment
            new_comment = st.text_input('Add a comment', key=f"comment_{idx}")
            if st.button('Submit Comment', key=f"submit_comment_{idx}"):
                if new_comment:
                    post['comments'].append(new_comment)
                    st.success('Comment added successfully!')
                else:
                    st.error('Please enter a comment before submitting.')
            
            st.write("---")

    # Footer
    st.markdown("""
    ---
    Created with ❤️ by team printf("Winners")
    """)


if __name__ == "__main__":
    crypto()