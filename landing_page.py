import streamlit as st
from main_page import main
from AI_Finance_Management import AIFM
from ai_assistant import ai_assistant
from game import game
from stock_price_prediction import stock

# Set the page title and layout
st.set_page_config(page_title="DJS-CSK World", layout="centered")

# Title of the landing page
st.title("Welcome to DJS-CSK World")

# Portfolio Button
if st.button("Portfolio"):
    main()

# Dropdown with 3 options
option = st.selectbox(
    "Choose a Feature",
    ("Select...", "Portfolio", "AI Finance Management", "AI Assistant","Game")
)

# Logic to handle dropdown selection
if option == "Portfolio":
    main()
elif option == "AI Finance Management":
    AIFM()
elif option == "AI Assistant":
    ai_assistant()
elif option == "Game":
    game()
