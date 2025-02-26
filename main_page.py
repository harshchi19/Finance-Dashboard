import streamlit as st
import side_bar as comp
import stTools as tools
import default_page
import portfolio_page
import model_page
import login_page


def main():
    st.title("Risk-O-Meter: Your Investment Safety Net")

    # Load sidebar (assumed to set load_portfolio_check and run_simulation_check via buttons)
    comp.load_sidebar()

    # Initialize session state flags if not present
    if "load_portfolio_check" not in st.session_state:
        st.session_state["load_portfolio_check"] = False

    if "run_simulation_check" not in st.session_state:
        st.session_state["run_simulation_check"] = False

    # Initialize demo stock data if not already set
    if "no_investment" not in st.session_state:
        st.session_state.no_investment = 8  # Number of stocks to initialize
        demo_stocks = ["AAPL", "AMZN", "TSLA", "META", "GOOG", "NVDA", "MSFT", "PYPL"]
        for i, ticker in enumerate(demo_stocks, 1):
            tools.create_stock_text_input(
                state_variable=f"stock_{i}_name",
                default_value=ticker,
                present_text=f"Stock {i} Ticker",
                key=f"stock{i}_input"
            )
            tools.create_date_input(
                state_variable=f"stock_{i}_purchase_date",
                present_text=f"Stock {i} Purchase Date",
                default_value="2023-01-01",
                key=f"date{i}_input"
            )
            # Initialize share quantity (required by build_portfolio in stTools.py)
            tools.create_state_variable(f"stock_{i}_share", 100)  # Default 100 shares

    # Page navigation logic
    if not st.session_state.load_portfolio_check:
        default_page.load_page()
    elif not st.session_state.run_simulation_check and st.session_state.load_portfolio_check:
        portfolio_page.load_page()
    elif st.session_state.run_simulation_check:
        model_page.load_page()


if __name__ == "__main__":
    main()
