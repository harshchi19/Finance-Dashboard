import streamlit as st
import side_bar as comp
import stTools as tools
import default_page
import portfolio_page
import model_page
import login_page

def main():
    
    st.title("Risk-O-Meter: Your Investment Safety Net")

    comp.load_sidebar()

    if "load_portfolio_check" not in st.session_state:
        st.session_state["load_portfolio_check"] = False

    if "run_simulation_check" not in st.session_state:
        st.session_state["run_simulation_check"] = False

    if not st.session_state.load_portfolio_check:
        default_page.load_page()

    elif not st.session_state.run_simulation_check and st.session_state.load_portfolio_check:
        portfolio_page.load_page()

    elif st.session_state.run_simulation_check:
        model_page.load_page()

if __name__ == "__main__":
    main()
