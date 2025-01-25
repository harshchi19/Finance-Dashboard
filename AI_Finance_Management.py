import google.generativeai as genai
import streamlit as st
import json
import pandas as pd

def AIFM():
    def initialize_session_state():
        return st.session_state.setdefault('api_key', None)

    st.title("AI Finance Management")
    st.title("By DJS-CSK")

    initialize_session_state()

    api_key = "AIzaSyAvRdlksakgf-bMoBBtC84Dxh2KqEkHUtQ"

    if not api_key:
        st.sidebar.error("API Error")
        st.stop()
    else:
        st.session_state.api_key = api_key

    genai.configure(api_key=api_key)

    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.9, 0.1)
    top_p = st.sidebar.number_input("Top P", 0.0, 1.0, 1.0, 0.1)
    top_k = st.sidebar.number_input("Top K", 1, 100, 1)
    max_output_tokens = st.sidebar.number_input("Max Output Tokens", 1, 10000, 2048)

    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_output_tokens,
    }

    safety_settings = "{}"
    safety_settings = json.loads(safety_settings)

    stable_income = st.radio("Do you have a stable income?", ("Yes", "No"))
    
    if stable_income == "Yes":
        income = st.number_input("Income (in Rupees):", min_value=0)
    else:
        income = 0

    expenses = st.number_input("Expenses (in Rupees):", min_value=0)
    essential_expense = st.number_input("Essential Expense (in Rupees):", min_value=0)
    non_essential_expense = st.number_input("Non-Essential Expense (in Rupees):", min_value=0)
    
    debt = st.radio("Do you have any debt?", ("Yes", "No"))
    
    if debt == "Yes":
        debt_amount = st.number_input("How much debt do you have? (in Rupees):", min_value=0)
        monthly_emi = st.number_input("Monthly EMI (in Rupees):", min_value=0)
        months_remaining = st.number_input("How many months are remaining on your EMI?", min_value=0)
    else:
        debt_amount = 0
        monthly_emi = 0
        months_remaining = 0

    savings_goal = st.number_input("How much amount do you want to save? (in Rupees):", min_value=0)
    current_saving = st.number_input("Current Saving (in Rupees):", min_value=0)
    months_to_achieve = st.number_input("In how many months do you want to achieve this saving?", min_value=0)

    custom_prompt = None
    if st.button("Custom Prompt"):
        custom_prompt = st.text_area("Enter additional information for the prompt:")

    if st.button("Generate Report"):
        prompt_parts = f"""
        Based on the following financial information (Please note: All monetary values are in INR and should be considered as is, without any multiplication or scaling):

        - Stable Income: {stable_income}
        - Monthly Income: {income} INR
        - Total Monthly Expenses: {expenses} INR
        - Essential Expenses: {essential_expense} INR
        - Non-Essential Expenses: {non_essential_expense} INR
        - Debt Status (have debt or not): {debt}
        - Total Debt: {debt_amount} INR
        - Monthly EMI: {monthly_emi} INR
        - Remaining EMI Months: {months_remaining}
        - Savings Goal: {savings_goal} INR
        - Current Savings: {current_saving} INR
        - Months to Achieve Savings Goal: {months_to_achieve}

        Please provide a comprehensive financial analysis in tabular format, including:

        1. Expense Tracking and Categorization: Break down essential vs. non-essential expenses as percentages of total income.
        2. Budgeting and Savings Goals: Suggest a monthly savings plan to reach the stated goal, accounting for current income and expenses.
        3. Debt Management: If applicable, outline a strategy to repay debt while balancing other financial goals.
        4. Monthly Savings Plan: Provide a month-by-month breakdown of recommended savings, considering debt repayment and the savings goal.
        5. Financial Health Overview: Summarize key financial ratios or metrics (e.g., debt-to-income ratio, savings rate) and their implications.

        Give all information in a wide, and precise table. Give a roadmap to achieve the saving goals and to repay debt which should be achieveable and break into months in tabular format. Provide brief explanations or recommendations where necessary to contextualize the data.
        NOTE : All the information must be in form of tables (no paragraphs, no pointers)
        """ 

        if custom_prompt:
            prompt_parts += f"\nAdditional Information: {custom_prompt}"

        try:
            gemini = genai.GenerativeModel(model_name="gemini-pro",
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)

            response = gemini.generate_content([prompt_parts])
            st.subheader("Response:")
            if response.text:
                st.write(response.text)
            else:
                st.write("No output from your financial advisor.")
        except Exception as e:
            st.write(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    AIFM()