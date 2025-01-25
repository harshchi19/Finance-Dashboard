import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random

def initialize_session_state():
    if 'banks' not in st.session_state:
        st.session_state['banks'] = {}
    if 'current_bank' not in st.session_state:
        st.session_state['current_bank'] = None
    if 'selected_option' not in st.session_state:
        st.session_state['selected_option'] = None

    if not st.session_state['banks']:
        add_fake_bank("Bank A")
        add_fake_bank("Bank B")
        st.session_state['current_bank'] = "Bank A"  

def add_fake_bank(bank_name):
    st.session_state['banks'][bank_name] = {
        'account_balance': round(random.uniform(5000, 20000), 2),
        'borrowings': [],
        'loans': [
            {
                'loan_id': 'LN001',
                'total_amount': 15000.0,
                'remaining_amount': 7000.0,
                'next_installment_date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                'next_installment_amount': 1000.0,
                'penalty': 0.0,
                'installment_history': [
                    {'date': (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'), 'amount': 1000.0},
                    {'date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'), 'amount': 1000.0},
                ]
            }
        ],
        'transaction_history': generate_fake_transactions(),
        'cards': [
            {'card_number': '1234567890123456', 'card_type': 'Debit', 'cvv': '123', 'last4': '3456'}
        ],
        'upi_ids': [
            {'upi_id': f'user{random.randint(1000,9999)}@upi', 'upi_pin': '1234'}
        ],
        'monthly_stats': {}
    }

def generate_fake_transactions():
    transactions = []
    modes = ['UPI', 'Card']
    categories = ['Payment', 'EMI', 'Groceries', 'Utilities', 'Entertainment']
    for _ in range(20):
        mode = random.choice(modes)
        category = random.choice(categories)
        amount = round(random.uniform(50, 5000), 2)
        date = datetime.now() - timedelta(days=random.randint(0, 365))
        transactions.append({
            'date': date.strftime('%Y-%m-%d'),
            'receiver': f'receiver{random.randint(1000,9999)}@upi' if mode == 'UPI' else f'**** **** **** {random.randint(1000,9999)}',
            'amount': amount,
            'mode': mode,
            'type': 'Sent' if random.choice([True, False]) else 'Received',
            'category': category
        })
    return transactions


def sidebar():
    st.sidebar.title("Banking Dashboard")
    
    # Send Money Feature in Sidebar
    if st.sidebar.button("Send Money"):
        st.session_state['selected_option'] = 'Send Money'
    
    st.sidebar.markdown("---")
    
    # Dropdown Menu for Options
    option = st.sidebar.selectbox(
        "Options",
        ("Select an Option", "Add UPI ID", "Add Card", "View Loans/Borrowings", "Switch/Add Bank", "Monthly Stats")
    )
    
    if option != "Select an Option":
        st.session_state['selected_option'] = option


def display_account_stats():
    bank = st.session_state['current_bank']
    bank_data = st.session_state['banks'][bank]

    st.title(f"{bank} Dashboard")

    # Hero Section
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Account Balance: ₹{bank_data['account_balance']:.2f}")
    with col2:
        st.markdown("")  # Placeholder for alignment

    st.markdown("---")

def display_transaction_history():
    bank = st.session_state['current_bank']
    transactions = st.session_state['banks'][bank]['transaction_history']

    if transactions:
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ascending=False)
        st.markdown("### Transaction History")
        st.dataframe(df[['date', 'receiver', 'amount', 'mode', 'type', 'category']].reset_index(drop=True))
        st.markdown("---")
    else:
        st.write("No transactions.")
        st.markdown("---")

def display_loan_borrowings():
    bank = st.session_state['current_bank']
    bank_data = st.session_state['banks'][bank]
    loans = bank_data['loans']
    borrowings = bank_data['borrowings']

    st.markdown("### Loans/Borrowings")

    st.subheader("Active Loans")
    if loans:
        for loan in loans:
            st.write(f"**Loan ID:** {loan['loan_id']}")
            st.write(f"**Loan Amount:** ₹{loan['total_amount']}")
            st.write(f"**Remaining Amount:** ₹{loan['remaining_amount']}")
            st.write(f"**Next Installment Date:** {loan['next_installment_date']}")
            st.write(f"**Next Installment Amount:** ₹{loan['next_installment_amount']}")
            st.write(f"**Penalty:** ₹{loan.get('penalty', 0)}")
            st.write("**Installment History:**")
            for installment in loan['installment_history']:
                st.write(f" - Date: {installment['date']}, Amount: ₹{installment['amount']}")
            st.markdown("---")
    else:
        st.write("No active loans.")

    st.subheader("Borrowings")
    if borrowings:
        for borrow in borrowings:
            st.write(borrow)
            st.markdown("---")
    else:
        st.write("No borrowings.")
        st.markdown("---")

def display_upis_cards():
    bank = st.session_state['current_bank']
    bank_data = st.session_state['banks'][bank]

    st.markdown("### UPI IDs")
    if bank_data['upi_ids']:
        for upi in bank_data['upi_ids']:
            st.write(upi['upi_id'])
    else:
        st.write("No UPI IDs added.")

    st.markdown("### Card Details")
    if bank_data['cards']:
        for card in bank_data['cards']:
            st.write(f"Card Number: **** **** **** {card['last4']}")
    else:
        st.write("No cards added.")

def add_upi_id():
    st.header("Add UPI ID")
    with st.form(key='add_upi_form'):
        upi_id = st.text_input("Enter UPI ID")
        upi_pin = st.text_input("Enter UPI PIN", type='password')
        submit_upi = st.form_submit_button("Add UPI ID")
        if submit_upi:
            if any(upi['upi_id'] == upi_id for upi in st.session_state['banks'][st.session_state['current_bank']]['upi_ids']):
                st.warning("UPI ID already exists.")
            else:
                st.session_state['banks'][st.session_state['current_bank']]['upi_ids'].append({
                    'upi_id': upi_id,
                    'upi_pin': upi_pin
                })
                st.success("UPI ID added successfully.")

def add_card():
    st.header("Add Debit/Credit Card")
    with st.form(key='add_card_form'):
        card_number = st.text_input("Enter Card Number")
        card_type = st.selectbox("Card Type", ["Debit", "Credit"])
        cvv = st.text_input("Enter CVV", type='password')
        submit_card = st.form_submit_button("Add Card")
        if submit_card:
            if not card_number.isdigit() or len(card_number) != 16:
                st.error("Invalid card number. It should be 16 digits.")
            elif not cvv.isdigit() or len(cvv) != 3:
                st.error("Invalid CVV. It should be 3 digits.")
            else:
                last4 = card_number[-4:]
                if any(card['last4'] == last4 for card in st.session_state['banks'][st.session_state['current_bank']]['cards']):
                    st.warning("Card already exists.")
                else:
                    st.session_state['banks'][st.session_state['current_bank']]['cards'].append({
                        'card_number': card_number,
                        'card_type': card_type,
                        'cvv': cvv,
                        'last4': last4
                    })
                    st.success("Card added successfully.")

def view_loans_borrowings():
    display_loan_borrowings()

def switch_add_bank():
    st.header("Switch/Add Bank")
    banks = list(st.session_state['banks'].keys())
    selected_bank = st.selectbox("Select Bank to Switch", options=banks)

    if selected_bank:
        st.session_state['current_bank'] = selected_bank
        st.success(f"Switched to {selected_bank} successfully.")

    st.markdown("---")
    st.subheader("Add a New Bank")
    with st.form(key='add_bank_form'):
        new_bank_name = st.text_input("Bank Name")
        submit_bank = st.form_submit_button("Add Bank")
        if submit_bank:
            if new_bank_name in st.session_state['banks']:
                st.warning("Bank already exists.")
            else:
                add_fake_bank(new_bank_name)
                st.success(f"Bank '{new_bank_name}' added successfully.")

def monthly_stats():
    st.header("Monthly Statistics")
    display_transaction_graphs()

def send_money():
    st.header("Send Money")
    bank = st.session_state['current_bank']
    bank_data = st.session_state['banks'][bank]

    with st.form(key='send_money_form'):
        receiver = st.text_input("Receiver UPI ID or Card Number")
        amount = st.number_input("Amount (₹)", min_value=1.0, step=1.0)
        mode = st.selectbox("Mode of Payment", ["Select Mode", "UPI", "Card"])

        selected_upi = None
        selected_card = None

        if mode == "UPI":
            if not bank_data['upi_ids']:
                st.error("Please add a UPI ID first and then send money.")
            else:
                selected_upi = st.selectbox("Select UPI ID", options=[upi['upi_id'] for upi in bank_data['upi_ids']])
        elif mode == "Card":
            if not bank_data['cards']:
                st.error("Please add a Card first and then send money.")
            else:
                selected_card = st.selectbox("Select Card", options=[f"**** **** **** {card['last4']}" for card in bank_data['cards']])

        if mode == "UPI" and bank_data['upi_ids']:
            pin = st.text_input("Enter UPI PIN", type='password')
        elif mode == "Card" and bank_data['cards']:
            cvv = st.text_input("Enter CVV", type='password')

        submit_payment = st.form_submit_button("Confirm Payment")

        if submit_payment:
            if mode not in ["UPI", "Card"]:
                st.error("Please select a valid mode of payment.")
                st.stop()
            if not receiver:
                st.error("Please enter the receiver's UPI ID or Card Number.")
                st.stop()
            if amount <= 0:
                st.error("Please enter a valid amount greater than 0.")
                st.stop()
            valid = False
            if mode == "UPI":
                for upi in bank_data['upi_ids']:
                    if upi['upi_id'] == selected_upi and upi['upi_pin'] == pin:
                        valid = True
                        break
                if not valid:
                    st.error("Invalid UPI PIN.")
            elif mode == "Card":
                for card in bank_data['cards']:
                    if f"**** **** **** {card['last4']}" == selected_card and card['cvv'] == cvv:
                        valid = True
                        break
                if not valid:
                    st.error("Invalid CVV.")

            if valid:
                if bank_data['account_balance'] >= amount:
                    bank_data['account_balance'] -= amount
                    transaction = {
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'receiver': receiver,
                        'amount': amount,
                        'mode': mode,
                        'type': 'Sent',
                        'category': 'Payment'
                    }
                    st.session_state['banks'][bank]['transaction_history'].append(transaction)
                    st.success("Payment successful.")
                    st.experimental_rerun() 
                else:
                    st.error("Insufficient balance.")


def display_transaction_graphs():
    bank = st.session_state['current_bank']
    transactions = st.session_state['banks'][bank]['transaction_history']

    if not transactions:
        st.write("No transactions to display.")
        return

    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M')
    df['day'] = df['date'].dt.day

    st.subheader("Spending by Mode")
    spend_mode = df[(df['type'] == 'Sent')]['amount'].groupby(df['mode']).sum()
    fig1, ax1 = plt.subplots()
    ax1.pie(spend_mode, labels=spend_mode.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

    st.subheader("Daily Spending in Current Month")
    current_month = datetime.now().strftime('%Y-%m')
    current_month_transactions = df[(df['type'] == 'Sent') & (df['month'].astype(str) == current_month)]
    daily_spending = current_month_transactions.groupby('day')['amount'].sum().sort_index()
    if not daily_spending.empty:
        fig2, ax2 = plt.subplots()
        daily_spending.plot(kind='bar', ax=ax2)
        ax2.set_xlabel("Day of Month")
        ax2.set_ylabel("Amount Spent (₹)")
        ax2.set_title("Daily Spending in Current Month")
        st.pyplot(fig2)
    else:
        st.write("No spending data available for the current month.")

def bank():
    
    initialize_session_state()
    sidebar()
    if not st.session_state['current_bank']:
        st.info("Please select a bank to continue.")
        select_or_add_bank()
        return  # Exit main to wait for user action
    selected_option = st.session_state.get('selected_option', None)

    if selected_option is None:
        display_account_stats()
        col1, col2 = st.columns(2)
        with col2:
            display_upis_cards()
        with col1:
            display_loan_borrowings()
        display_transaction_history()
        st.markdown("---")
    else:
        if selected_option == "Add UPI ID":
            add_upi_id()
        elif selected_option == "Add Card":
            add_card()
        elif selected_option == "View Loans/Borrowings":
            view_loans_borrowings()
        elif selected_option == "Switch/Add Bank":
            switch_add_bank()
        elif selected_option == "Monthly Stats":
            monthly_stats()
        elif selected_option == "Send Money":
            send_money()

    if selected_option in ["Add UPI ID", "Add Card", "View Loans/Borrowings", "Switch/Add Bank", "Monthly Stats", "Send Money"]:
        st.session_state['selected_option'] = None

def select_or_add_bank():
    st.header("Select or Add Your Bank")
    banks = list(st.session_state['banks'].keys())
    selected_bank = st.selectbox("Choose your bank", options=banks)

    if selected_bank:
        st.session_state['current_bank'] = selected_bank
        st.success(f"Switched to {selected_bank} successfully.")

    st.markdown("---")
    st.subheader("Add a New Bank")
    with st.form(key='add_bank_form_initial'):
        new_bank_name = st.text_input("Bank Name")
        submit_bank = st.form_submit_button("Add Bank")
        if submit_bank:
            if new_bank_name in st.session_state['banks']:
                st.warning("Bank already exists.")
            elif new_bank_name.strip() == "":
                st.warning("Bank name cannot be empty.")
            else:
                add_fake_bank(new_bank_name)
                st.success(f"Bank '{new_bank_name}' added successfully.")
                st.session_state['current_bank'] = new_bank_name  # Automatically switch to the new bank
                st.experimental_rerun()  # Refresh the page to display the new bank's dashboard

if __name__ == "__main__":
    bank()
