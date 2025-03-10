import datetime
import streamlit as st
import yfinance as yf
import datetime as dt
from assets.Collector import InfoCollector
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
from assets import Portfolio
from assets import Stock
import plotly.express as px


def create_state_variable(key: str, default_value: any) -> None:
    if key not in st.session_state:
        st.session_state[key] = default_value


def create_stock_text_input(
        state_variable: str,
        default_value: str,
        present_text: str,
        key: str
) -> None:
    create_state_variable(state_variable, default_value)
    st.session_state[state_variable] = st.text_input(present_text,
                                                     key=key,
                                                     value=st.session_state[state_variable])


def create_date_input(
        state_variable: str,
        present_text: str,
        default_value: str,
        key: str
) -> None:
    create_state_variable(state_variable, default_value)
    st.session_state[state_variable] = st.date_input(present_text,
                                                     value=st.session_state[state_variable],
                                                     key=key)


def get_stock_demo_data(no_stocks: int) -> list:
    stock_name_list = ['AAPL', 'TSLA', 'GOOG', 'MSFT',
                       'AMZN', 'META', 'NVDA', 'PYPL',
                       'NFLX', 'ADBE', 'INTC', 'CSCO']
    return stock_name_list[:no_stocks]


def click_button_sim() -> None:
    st.session_state["run_simulation"] = True
    st.session_state["run_simulation_check"] = True


def click_button_port() -> None:
    st.session_state["load_portfolio"] = True
    st.session_state["load_portfolio_check"] = True
    st.session_state["run_simulation_check"] = False


def preview_stock(
        session_state_name: str,
        start_date: datetime.datetime
) -> None:
    """
    Display a preview of the stock's performance since purchase.
    
    Args:
        session_state_name (str): The stock ticker symbol (e.g., "AAPL").
        start_date (datetime.datetime): The purchase date to start tracking from.
    """
    try:
        # Fetch stock data
        stock_data = yf.download(session_state_name,
                                 start=start_date,
                                 end=dt.datetime.now())
        if stock_data.empty:
            st.write(f"No data available for {session_state_name} since {start_date}.")
            return
        
        # Select only Close column and reset index
        stock_data = stock_data[['Close']].reset_index(drop=True)
        
        # Ensure scalar values for price difference
        purchase_price = stock_data['Close'].iloc[0].item()  # First close price
        current_price = stock_data['Close'].iloc[-1].item()  # Last close price
        diff_price = current_price - purchase_price          # Scalar difference

        # Set color based on price difference
        color = '#8080809e'  # Default gray
        if diff_price > 0.0:
            color = '#00fa119e'  # Green for gain
        elif diff_price < 0.0:
            color = '#fa00009e'  # Red for loss

        # Add days since buy as a column
        stock_data['day(s) since buy'] = range(0, len(stock_data))

        # Create metric card (this part works fine)
        create_metric_card(label=session_state_name,
                           value=f"{current_price:.2f}",
                           delta=f"{diff_price:.2f}")

        # Attempt to display area chart, silently ignoring errors
        try:
            st.area_chart(stock_data, x='day(s) since buy', y='Close',
                          use_container_width=True, height=250, color=color)
        except:
            pass  # Ignore chart-related errors silently

    except Exception as e:
        # Only catch critical errors (e.g., data fetching), but still show metric card if possible
        st.write(f"No data available for {session_state_name} due to an error: {str(e)}")


def format_currency(number: float) -> str:
    return "${:,.2f}".format(number)


def create_side_bar_width() -> None:
    st.markdown(
        """
       <style>
       [data-testid="stSidebar"][aria-expanded="true"]{
           min-width: 450px;
           max-width: 600px;
       }
       """,
        unsafe_allow_html=True,
    )


def remove_white_space():
    st.markdown("""
            <style>
                   .block-container {
                        padding-top: 1rem;
                    }
            </style>
            """, unsafe_allow_html=True)


def get_current_date() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d')


def create_candle_stick_plot(stock_ticker_name: str, stock_name: str) -> None:
    stock = InfoCollector.get_ticker(stock_ticker_name)
    stock_data = InfoCollector.get_history(stock, period="1d", interval='5m')
    stock_data_template = InfoCollector.get_demo_daily_history(interval='5m')

    stock_data = stock_data[['Open', 'High', 'Low', 'Close']]

    open_price = stock_data.iloc[0]['Open']
    close_price = InfoCollector.get_history(stock, period="1d")["Close"].item()
    diff_price = close_price - open_price

    create_metric_card(label=stock_name,
                       value=f"{close_price:.2f}",
                       delta=f"{diff_price:.2f}")

    candlestick_chart = go.Figure(data=[
        go.Candlestick(x=stock_data_template.index,
                       open=stock_data['Open'],
                       high=stock_data['High'],
                       low=stock_data['Low'],
                       close=stock_data['Close'])])
    candlestick_chart.update_layout(xaxis_rangeslider_visible=False,
                                    margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(candlestick_chart, use_container_width=True, height=100)


def create_stocks_dataframe(stock_ticker_list: list, stock_name: list) -> pd.DataFrame:
    close_price = []
    daily_change = []
    pct_change = []
    all_price = []
    for stock_ticker in stock_ticker_list:
        stock = InfoCollector.get_ticker(stock_ticker)
        stock_data = InfoCollector.get_history(stock, period="1d", interval='5m')
        
        close_price_value = round(stock_data.iloc[-1]['Close'], 2)
        close_price.append(close_price_value)

        daily_change_value = round(stock_data.iloc[-1]['Close'] - stock_data.iloc[0]['Open'], 2)
        daily_change.append(daily_change_value)

        pct_change_value = round((stock_data.iloc[-1]['Close'] - stock_data.iloc[0]['Open'])
                                 / stock_data.iloc[0]['Open'] * 100, 2)
        pct_change.append(pct_change_value)

        all_price.append(stock_data['Close'].tolist())

    df_stocks = pd.DataFrame(
        {
            "stock_tickers": stock_ticker_list,
            "stock_name": stock_name,
            "close_price": close_price,
            "daily_change": daily_change,
            "pct_change": pct_change,
            "views_history": all_price
        }
    )
    return df_stocks


def win_highlight(val: str) -> str:
    color = None
    val = str(val).replace(',', '')
    if float(val) >= 0.0:
        color = '#00fa119e'
    elif float(val) < 0.0:
        color = '#fa00009e'
    return f'background-color: {color}'


def create_dateframe_view(df: pd.DataFrame) -> None:
    df['close_price'] = df['close_price'].apply(lambda x: f'{x:,.2f}')
    df['daily_change'] = df['daily_change'].apply(lambda x: f'{x:,.2f}')
    df['pct_change'] = df['pct_change'].apply(lambda x: f'{x:,.2f}')

    st.dataframe(
        df.style.applymap(win_highlight,
                          subset=['daily_change', 'pct_change']),
        column_config={
            "stock_tickers": "Tickers",
            "stock_name": "Stock",
            "close_price": "Price ($)",
            "daily_change": "Price Change ($)",
            "pct_change": "% Change",
            "views_history": st.column_config.LineChartColumn("daily trend"),
        },
        hide_index=True,
        width=620,
    )


def build_portfolio(no_stocks: int) -> Portfolio.Portfolio:
    my_portfolio = Portfolio.Portfolio()
    for i in range(no_stocks):
        stock = Stock.Stock(stock_name=st.session_state[f"stock_{i + 1}_name"])
        stock.add_buy_action(quantity=int(st.session_state[f"stock_{i + 1}_share"]),
                             purchase_date=st.session_state[f"stock_{i + 1}_purchase_date"])
        my_portfolio.add_stock(stock=stock)
    return my_portfolio


def get_metric_bg_color() -> str:
    return "#282C35"


def create_metric_card(label: str, value: str, delta: str) -> None:
    st.metric(label=label, value=value, delta=delta)
    background_color = get_metric_bg_color()
    style_metric_cards(background_color=background_color)


def create_pie_chart(key_values: dict) -> None:
    labels = list(key_values.keys())
    values = list(key_values.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                                 insidetextorientation='radial')])
    fig.update_layout(xaxis_rangeslider_visible=False,
                      margin=dict(l=20, r=20, t=20, b=20),
                      showlegend=False)
    st.plotly_chart(fig, use_container_width=True, use_container_height=True)


def create_line_chart(portfolio_df: pd.DataFrame) -> None:
    fig = px.line(portfolio_df)
    fig.update_layout(xaxis_rangeslider_visible=False,
                      margin=dict(l=20, r=20, t=20, b=20),
                      showlegend=False,
                      xaxis_title="Day(s) since purchase",
                      yaxis_title="Portfolio Value ($)")
    st.plotly_chart(fig, use_container_width=True, use_container_height=True)
