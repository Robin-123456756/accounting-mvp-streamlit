
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="Accounting MVP", layout="wide", page_icon="💰")

# Theme: Orange and White
st.markdown(
    '''
    <style>
    .main {background-color: #ffffff;}
    h1, h2, h3, h4 {color: #ff6f00;}
    .stButton>button {background-color: #ff6f00; color: white;}
    </style>
    ''',
    unsafe_allow_html=True
)

# Initial setup
DATA_DIR = "data"
INVOICE_FILE = os.path.join(DATA_DIR, "invoices.csv")
EXPENSE_FILE = os.path.join(DATA_DIR, "expenses.csv")

# Ensure data files exist
if not os.path.exists(INVOICE_FILE):
    pd.DataFrame(columns=["Date", "Client", "Description", "Amount (UGX)"]).to_csv(INVOICE_FILE, index=False)

if not os.path.exists(EXPENSE_FILE):
    pd.DataFrame(columns=["Date", "Category", "Description", "Amount (UGX)"]).to_csv(EXPENSE_FILE, index=False)

st.title("📊 Accounting Dashboard (UGX)")

tab1, tab2, tab3, tab4 = st.tabs(["➕ Invoices", "➖ Expenses", "📈 Reports", "📥 Export"])

with tab1:
    st.subheader("Add Invoice")
    with st.form("invoice_form"):
        client = st.text_input("Client Name")
        desc = st.text_input("Description")
        amount = st.number_input("Amount (UGX)", min_value=0)
        submitted = st.form_submit_button("Save Invoice")
        if submitted:
            new = pd.DataFrame([[datetime.now(), client, desc, amount]], columns=["Date", "Client", "Description", "Amount (UGX)"])
            existing = pd.read_csv(INVOICE_FILE)
            existing = pd.concat([existing, new], ignore_index=True)
            existing.to_csv(INVOICE_FILE, index=False)
            st.success("Invoice saved!")

with tab2:
    st.subheader("Log Expense")
    with st.form("expense_form"):
        category = st.selectbox("Category", ["Office", "Transport", "Supplies", "Other"])
        desc = st.text_input("Description")
        amount = st.number_input("Amount (UGX)", min_value=0)
        submitted = st.form_submit_button("Save Expense")
        if submitted:
            new = pd.DataFrame([[datetime.now(), category, desc, amount]], columns=["Date", "Category", "Description", "Amount (UGX)"])
            existing = pd.read_csv(EXPENSE_FILE)
            existing = pd.concat([existing, new], ignore_index=True)
            existing.to_csv(EXPENSE_FILE, index=False)
            st.success("Expense saved!")

with tab3:
    st.subheader("Reports")
    invoices = pd.read_csv(INVOICE_FILE)
    expenses = pd.read_csv(EXPENSE_FILE)
    total_income = invoices["Amount (UGX)"].sum()
    total_expense = expenses["Amount (UGX)"].sum()
    profit = total_income - total_expense
    st.metric("Total Income", f"{total_income:,.0f} UGX")
    st.metric("Total Expenses", f"{total_expense:,.0f} UGX")
    st.metric("Net Profit", f"{profit:,.0f} UGX")

    with st.expander("View Details"):
        st.write("### Invoices")
        st.dataframe(invoices)
        st.write("### Expenses")
        st.dataframe(expenses)

with tab4:
    st.subheader("Export Data")
    with open(INVOICE_FILE, "rb") as f:
        st.download_button("Download Invoices CSV", f, "invoices.csv")
    with open(EXPENSE_FILE, "rb") as f:
        st.download_button("Download Expenses CSV", f, "expenses.csv")
