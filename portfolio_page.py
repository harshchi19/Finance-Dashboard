import streamlit as st
import stTools as tools
import portfolio_page_components


def load_page():
    # Ensure no_stocks is initialized in session state
    if 'no_investment' not in st.session_state:
        st.session_state.no_investment = 0  # Default to 0 if not set
    no_stocks = st.session_state.no_investment

    # Load portfolio performance
    my_portfolio = tools.build_portfolio(no_stocks=no_stocks)
    my_portfolio.update_market_value()

    portfolio_book_amount = my_portfolio.book_amount
    portfolio_market_value = my_portfolio.market_value
    diff_amount = portfolio_market_value - portfolio_book_amount
    
    # Avoid division by zero
    if portfolio_book_amount != 0:
        pct_change = (diff_amount / portfolio_book_amount) * 100
    else:
        pct_change = 0.0

    # Save my_portfolio to session state
    st.session_state.my_portfolio = my_portfolio

    # Create 2 columns for layout
    col1_summary, col2_pie = st.columns(2)

    with col1_summary:
        portfolio_page_components.load_portfolio_performance_cards(
            portfolio_book_amount=portfolio_book_amount,
            portfolio_market_value=portfolio_market_value,
            diff_amount=diff_amount,
            pct_change=pct_change
        )

    with col2_pie:
        portfolio_page_components.load_portfolio_summary_pie()

    # Load portfolio summary
    portfolio_page_components.load_portfolio_summary_table()

    # Load investment preview
    if no_stocks > 0:  # Only show preview if there are stocks
        st.subheader("Investment Performance Summary - Since Purchase")
        portfolio_page_components.load_portfolio_preview(no_stocks=no_stocks)
    else:
        st.write("No investments to preview yet.")
