import streamlit as st
import stTools as tools


def load_page():
    st.markdown(
        """
           Welcome to Risk-O-Meter! Are you ready to take the guesswork out of your investments? Our app uses advanced risk management tools like Value at Risk (VaR) and Conditional Value at Risk (CVaR) to help you understand and minimize potential losses. Think of it as a safety net for your financial journey
            """
    )

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

            [data-testid="stMetric"]{
                background-color: #FFF !important;}
    </style>
        """, unsafe_allow_html=True)

    st.subheader(f"Market Preview")

    col_stock1, col_stock_2, col_stock_3 = st.columns(3)

    with col_stock1:
        tools.create_candle_stick_plot(stock_ticker_name="^DJI",
                                       stock_name="Dow Jones Industrial")

    with col_stock_2:
        tools.create_candle_stick_plot(stock_ticker_name="^IXIC",
                                       stock_name="Nasdaq Composite")

    with col_stock_3:
        tools.create_candle_stick_plot(stock_ticker_name="^GSPC",
                                       stock_name="S&P 500")

    # make 3 columns for sectors
    col_sector1, col_sector2, col_sector3 = st.columns(3)

    with col_sector1:
        st.subheader(f"Technology")
        stock_list = ["AAPL", "MSFT", "AMZN", "GOOG", "META", "TSLA", "NVDA", "NFLX"]
        stock_name = ["Apple", "Microsoft", "Amazon", "Google", "Meta", "Tesla", "Nvidia", "Netflix"]

        df_stocks = tools.create_stocks_dataframe(stock_list, stock_name)
        tools.create_dateframe_view(df_stocks)

    with col_sector2:
        st.subheader(f"Banking")
        stock_list = ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC']
        stock_name = ['JPMorgan', 'BoA', 'Wells Fargo', 'Goldman Sachs', 'Morgan Stanley',
                       'Citigroup', 'U.S. Bancorp', 'PNC']
        df_stocks = tools.create_stocks_dataframe(stock_list, stock_name)
        tools.create_dateframe_view(df_stocks)

    with col_sector3:
        st.subheader(f"Meme Stocks")
        stock_list = ["GME", "AMC", "BB", "NOK", "RIVN", "SPCE", "F", "T"]
        stock_name = ["GameStop", "AMC Entertainment", "BlackBerry", "Nokia", "Rivian",
                      "Virgin Galactic", "Ford", "AT&T"]

        df_stocks = tools.create_stocks_dataframe(stock_list, stock_name)
        tools.create_dateframe_view(df_stocks)