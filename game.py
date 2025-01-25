import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def game():

    def set_background(image_url):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url({image_url});
                background-size: cover;
                background-position: top;
                background-repeat:repeat;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    set_background("https://t4.ftcdn.net/jpg/02/04/62/55/360_F_204625568_DstbVm1f5H2vw3RsqUf78tTEf8mavgBz.jpg")
    
    st.markdown("""
    <style>
            html{
                font-family: Manrope;
                }
            .e1nzilvr2{
                text-align:center;
                text-shadow: 0px 2px 5.3px rgba(0, 0, 0, 0.19);
                font-family: Manrope;
                font-size: 92px;
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
    
    # Initialize session state variables
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {}
    if 'cash' not in st.session_state:
        st.session_state.cash = 10000  # Starting cash
    if 'transactions' not in st.session_state:
        st.session_state.transactions = []
    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = {}

    def get_stock_price(symbol):
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if not data.empty:
            return data['Close'].iloc[-1]
        return None

    def get_stock_data(symbol, period="1mo"):
        if symbol not in st.session_state.stock_data:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            st.session_state.stock_data[symbol] = data
        return st.session_state.stock_data[symbol]

    def buy_stock(symbol, amount):
        price = get_stock_price(symbol)
        if price is None:
            st.error(f"Could not fetch price for {symbol}")
            return

        cost = price * amount
        if cost > st.session_state.cash:
            st.error("Not enough cash for this transaction")
            return

        st.session_state.cash -= cost
        if symbol in st.session_state.portfolio:
            st.session_state.portfolio[symbol] += amount
        else:
            st.session_state.portfolio[symbol] = amount

        st.session_state.transactions.append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'BUY',
            'symbol': symbol,
            'amount': amount,
            'price': price
        })
        st.success(f"Bought {amount} shares of {symbol} at ${price:.2f} per share")
        get_stock_data(symbol)  # Fetch stock data for the graph

    def sell_stock(symbol, amount):
        if symbol not in st.session_state.portfolio or st.session_state.portfolio[symbol] < amount:
            st.error("Not enough shares to sell")
            return

        price = get_stock_price(symbol)
        if price is None:
            st.error(f"Could not fetch price for {symbol}")
            return

        st.session_state.cash += price * amount
        st.session_state.portfolio[symbol] -= amount
        if st.session_state.portfolio[symbol] == 0:
            del st.session_state.portfolio[symbol]

        st.session_state.transactions.append({
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': 'SELL',
            'symbol': symbol,
            'amount': amount,
            'price': price
        })
        st.success(f"Sold {amount} shares of {symbol} at ${price:.2f} per share")

    def calculate_portfolio_value():
        value = st.session_state.cash
        for symbol, amount in st.session_state.portfolio.items():
            price = get_stock_price(symbol)
            if price is not None:
                value += price * amount
        return value

    def create_portfolio_graph():
        fig = go.Figure()
        for symbol, amount in st.session_state.portfolio.items():
            price = get_stock_price(symbol)
            if price is not None:
                fig.add_trace(go.Bar(
                    x=[symbol],
                    y=[price * amount],
                    name=symbol
                ))

        fig.update_layout(
            title="Portfolio Composition",
            xaxis_title="Stock Symbol",
            yaxis_title="Value ($)",
            showlegend=True
        )
        return fig

    def create_stock_price_graph():
        fig = go.Figure()
        for symbol in st.session_state.portfolio.keys():
            data = get_stock_data(symbol)
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                mode='lines',
                name=symbol
            ))

        fig.update_layout(
            title="Stock Price History",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            showlegend=True
        )
        return fig

    st.title("🚀 Stock Market Simulator")
    st.write("Practice trading stocks with $10,000 of fake money!")

    # Sidebar for user actions
    st.sidebar.header("Trading Actions")
    action = st.sidebar.selectbox("Choose an action", ["Buy", "Sell"])
    symbol = st.sidebar.text_input("Enter stock symbol (e.g., AAPL, GOOGL)").upper()
    amount = st.sidebar.number_input("Enter number of shares", min_value=1, value=1)

    if st.sidebar.button("Execute Trade"):
        if action == "Buy":
            buy_stock(symbol, amount)
        else:
            sell_stock(symbol, amount)

    # Display portfolio
    st.header("Your Portfolio")
    portfolio_df = pd.DataFrame([(symbol, amount, get_stock_price(symbol), amount * get_stock_price(symbol)) 
                                 for symbol, amount in st.session_state.portfolio.items()],
                                columns=["Symbol", "Shares", "Current Price", "Total Value"])
    portfolio_df.set_index("Symbol", inplace=True)
    st.dataframe(portfolio_df)

    # Display portfolio graph
    if st.session_state.portfolio:
        st.plotly_chart(create_portfolio_graph())

    # Display stock price graph
    if st.session_state.portfolio:
        st.plotly_chart(create_stock_price_graph())

    # Display cash and total value
    total_value = calculate_portfolio_value()
    st.write(f"Available Cash: ${st.session_state.cash:.2f}")
    st.markdown(f"<h2 style='text-align: center; color: green;'>Total Portfolio Value: ${total_value:.2f}</h2>", unsafe_allow_html=True)

    # Display recent transactions
    st.header("Recent Transactions")
    transactions_df = pd.DataFrame(st.session_state.transactions[-5:])  # Show last 5 transactions
    if not transactions_df.empty:
        transactions_df = transactions_df[::-1]  # Reverse order to show most recent first
        st.table(transactions_df)

    # Stock price checker
    st.header("Stock Price Checker")
    check_symbol = st.text_input("Enter a stock symbol to check its price").upper()
    if st.button("Check Price"):
        price = get_stock_price(check_symbol)
        if price is not None:
            st.write(f"Current price of {check_symbol}: ${price:.2f}")
        else:
            st.error(f"Could not fetch price for {check_symbol}")

if __name__ == "__main__":
    game()