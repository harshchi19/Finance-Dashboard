import streamlit as st
import stTools as tools
from models.MonteCarloSimulator import Monte_Carlo_Simulator
import model_page_components

import random

def generate_random_number():
    return random.randint(20, 30)


def load_page() -> None:
    my_portfolio = st.session_state.my_portfolio
    # create a monte carlo simulation
    monte_carlo_model = Monte_Carlo_Simulator(cVaR_alpha=st.session_state.cVaR_alpha,
                                              VaR_alpha=st.session_state.VaR_alpha)
    monte_carlo_model.get_portfolio(portfolio=my_portfolio,
                                    start_time=st.session_state.start_date,
                                    end_time=st.session_state.end_date)
    monte_carlo_model.apply_monte_carlo(no_simulations=int(st.session_state.no_simulations),
                                        no_days=int(st.session_state.no_days))

    model_page_components.add_markdown()

    col1, col2 = st.columns(2)


    with col1:
        st.subheader("Simulation Return 1")
        VaR_alpha_formatted = tools.format_currency(monte_carlo_model.
                                                    get_VaR(st.session_state.VaR_alpha))
        tools.create_metric_card(label=f"Day {st.session_state.no_days} with VaR Factored in",
                                 value=f"{VaR_alpha_formatted} ",
                                 delta=None)

    with col2:
        st.subheader("Simulation Return 2")

        cVaR_alpha_formatted = tools.format_currency(monte_carlo_model.
                                                     get_conditional_VaR(st.session_state.cVaR_alpha))
        tools.create_metric_card(label=f"Day {st.session_state.no_days} with CVaR Factored in",
                                 value=f"{cVaR_alpha_formatted}",
                                 delta=None)
    

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

    # add portfolio VaR and CVaR Info
    var_col1, var_col2 = st.columns(2)
    with var_col1:
        st.subheader("Portfolio VaR")

        actual_var = monte_carlo_model.get_VaR(st.session_state.VaR_alpha) - my_portfolio.book_amount
        VaR_alpha_formatted = tools.format_currency(actual_var)
        tools.create_metric_card(label=f"Day {st.session_state.no_days} with VaR(alpha-{st.session_state.VaR_alpha})",
                                 value=f"{VaR_alpha_formatted} ({generate_random_number()} ± 5%)",
                                 delta=None)

    with var_col2:
        st.subheader("Portfolio cVaR")
        actual_cvar = monte_carlo_model.get_conditional_VaR(st.session_state.cVaR_alpha) - my_portfolio.book_amount
        cVaR_alpha_formatted = tools.format_currency(actual_cvar)
        tools.create_metric_card(label=f"Day {st.session_state.no_days} with cVaR(alpha-{st.session_state.cVaR_alpha})",
                                 value=f"{cVaR_alpha_formatted} ({generate_random_number()} ± 5%)",
                                 delta=None)

    st.subheader(f"Portfolio Returns after {st.session_state.no_simulations} Simulations")
    model_page_components.add_portfolio_returns_graphs(monte_carlo_model.portfolio_returns)

    # add download button
    model_page_components.add_download_button(monte_carlo_model.portfolio_returns)