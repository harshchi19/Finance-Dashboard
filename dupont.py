import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

def dupont():
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


    set_background("https://img.freepik.com/free-vector/geometric-pattern-background-vector-white_53876-126684.jpg")
    st.title("DuPont Analysis Calculator")
    st.write("""
    DuPont analysis breaks down Return on Equity (ROE) into three components: 
    profit margin, asset turnover, and financial leverage. It helps identify the sources of a company's ROE.
    """)
    st.markdown("*ROE = (Net Income / Revenue) * (Revenue / Total Assets) * (Total Assets / Shareholders' Equity)*")

    ticker = st.text_input("Enter Stock Ticker:", value="AAPL")

    def get_financial_data(ticker):
        stock = yf.Ticker(ticker)
        
        # Get income statement for the last 4 quarters
        income_stmt = stock.quarterly_financials.T.iloc[:4].sum()
        
        # Get latest balance sheet
        balance_sheet = stock.balance_sheet.T.iloc[0]
        
        return income_stmt, balance_sheet

    def safe_divide(a, b):
        if pd.isna(a) or pd.isna(b) or b == 0:
            return np.nan
        return a / b

    def approximate_value(value, default, label):
        if pd.isna(value) or value == 0:
            st.warning(f"{label} data is missing or zero. Using approximation.")
            return default
        return value

    if st.button("Calculate ROE"):
        try:
            # Fetch financial data
            income_stmt, balance_sheet = get_financial_data(ticker)
            
            # Extract and approximate required values
            net_income = approximate_value(income_stmt.get("Net Income"), income_stmt.get("Gross Profit", 0) * 0.1, "Net Income")
            revenue = approximate_value(income_stmt.get("Total Revenue"), net_income * 10, "Revenue")
            total_assets = approximate_value(balance_sheet.get("Total Assets"), revenue * 2, "Total Assets")
            total_liabilities = approximate_value(balance_sheet.get("Total Liab"), total_assets * 0.5, "Total Liabilities")
            total_equity = approximate_value(balance_sheet.get("Total Stockholder Equity"), total_assets - total_liabilities, "Shareholders' Equity")
            
            # Calculate components
            profit_margin = safe_divide(net_income, revenue)
            asset_turnover = safe_divide(revenue, total_assets)
            financial_leverage = safe_divide(total_assets, total_equity)
            
            # Calculate ROE
            roe = profit_margin * asset_turnover * financial_leverage
            
            # Create a DataFrame for the results
            results_df = pd.DataFrame({
                'Metric': ['Net Income', 'Revenue', 'Total Assets', "Shareholders' Equity",
                           'Profit Margin', 'Asset Turnover', 'Financial Leverage', 'Return on Equity (ROE)'],
                'Value': [f"${net_income:,.2f}", f"${revenue:,.2f}", f"${total_assets:,.2f}", f"${total_equity:,.2f}",
                          f"{profit_margin:.2%}", f"{asset_turnover:.2f}", f"{financial_leverage:.2f}", f"{roe:.2%}"]
            })
            
            # Display results in a table
            st.table(results_df)
            
            # Display the calculation
            st.write("ROE Calculation:")
            st.write(f"({net_income:,.2f} / {revenue:,.2f}) * ({revenue:,.2f} / {total_assets:,.2f}) * ({total_assets:,.2f} / {total_equity:,.2f}) = {roe:.2%}")
            
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    dupont()