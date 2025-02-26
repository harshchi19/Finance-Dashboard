import streamlit as st
import stTools as tools
import pandas as pd


def load_portfolio_performance_cards(
        portfolio_book_amount: float,
        portfolio_market_value: float,
        diff_amount: float,
        pct_change: float
) -> None:
    """
    Display portfolio performance metrics in metric cards.
    
    Args:
        portfolio_book_amount (float): Total book cost of the portfolio.
        portfolio_market_value (float): Current market value of the portfolio.
        diff_amount (float): Difference between market value and book cost.
        pct_change (float): Percentage change in portfolio value.
    """
    st.subheader("Portfolio Performance")
    tools.create_metric_card(label="Book Cost of Portfolio",
                             value=tools.format_currency(portfolio_book_amount),
                             delta=None)
    tools.create_metric_card(label="Market Value of Portfolio",
                             value=tools.format_currency(portfolio_market_value),
                             delta=None)
    tools.create_metric_card(label="Gain/Loss on Investments Unrealized",
                             value=tools.format_currency(diff_amount),
                             delta=f"{pct_change:.2f}%")


def load_portfolio_summary_pie() -> None:
    """
    Display a pie chart showing the portfolio distribution by book cost.
    """
    st.subheader("Portfolio Distribution")
    if 'my_portfolio' not in st.session_state or not st.session_state.my_portfolio.stocks:
        st.write("No portfolio data available yet.")
        return
    
    book_cost_list = {}
    for stock in st.session_state.my_portfolio.stocks.values():
        book_cost_list[stock.stock_name] = stock.get_book_cost()

    # Create pie chart
    tools.create_pie_chart(book_cost_list)


def load_portfolio_summary_table() -> None:
    """
    Display a table summarizing portfolio details including book cost, market value,
    gain/loss, and percentage change for each stock.
    """
    st.subheader("Portfolio Summary")
    if 'my_portfolio' not in st.session_state or not st.session_state.my_portfolio.stocks:
        st.write("No portfolio data available yet.")
        return

    # Build stock info dictionary
    stock_info = {}
    for stock in st.session_state.my_portfolio.stocks.values():
        book_cost = round(stock.get_book_cost(), 2)
        market_value = round(stock.get_market_value(), 2)
        gain_loss = round(market_value - book_cost, 2)
        # Handle division by zero
        pct_change = round((gain_loss / book_cost * 100) if book_cost != 0 else 0.0, 2)

        stock_info[stock.stock_name] = [book_cost, market_value, gain_loss, pct_change]

    # Create DataFrame
    column_names = ['Book Cost', 'Market Value', 'Gain/Loss', '% Change']
    stock_df = pd.DataFrame.from_dict(stock_info,
                                      orient='index',
                                      columns=column_names)
    stock_df.index.name = 'Stock'

    # Format columns with commas and 2 decimal places
    for column in stock_df.columns:
        stock_df[column] = stock_df[column].apply(lambda x: f'{x:,.2f}')

    # Display styled DataFrame
    st.dataframe(
        stock_df.style.map(tools.win_highlight,
                           subset=['Gain/Loss', '% Change']),
        column_config={
            "Stock": "Ticker",
            "Book Cost": "Book Cost($)",
            "Market Value": "Market Value($)",
            "Gain/Loss": "Gain/Loss($)",  # Positive = green, negative = red
            "% Change": "% Change",      # Positive = green, negative = red
        },
        hide_index=False,  # Show stock names in the index
        width=600,         # Reasonable width for readability
    )


def load_portfolio_preview(no_stocks: int) -> None:
    """
    Display a preview of each stock's performance since purchase in a 4-column layout.
    
    Args:
        no_stocks (int): Number of stocks in the portfolio.
    """
    if no_stocks <= 0:
        st.write("No stocks to preview.")
        return

    column_limit = 4
    # Create 4 columns for layout
    col_stock1, col_stock_2, col_stock_3, col_stock_4 = st.columns(column_limit)
    columns_list = [col_stock1, col_stock_2, col_stock_3, col_stock_4]

    columns_no = 0
    for i in range(no_stocks):
        stock_key = f"stock_{i + 1}_name"
        date_key = f"stock_{i + 1}_purchase_date"
        
        # Validate session state keys
        if stock_key not in st.session_state or date_key not in st.session_state:
            st.error(f"Missing data for {stock_key} or {date_key}. Please ensure stock details are initialized.")
            continue

        if columns_no == column_limit:
            columns_no = 0
        with columns_list[columns_no]:
            # Pass stock ticker and purchase date to preview_stock
            tools.preview_stock(st.session_state[stock_key],
                                start_date=st.session_state[date_key])
        columns_no += 1
