import streamlit as st
import pandas as pd
import os
from datetime import date

# ------------------ BASIC SETUP ------------------
st.set_page_config(
    page_title="Personal Finance Manager",
    layout="wide"
)

st.title("Personal Finance Management System")
st.caption("Income | Expenses | Investments | Loans — Unified Dashboard")

USERS = ["Ritika", "Himanshu", "Seema"]

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "income": f"{DATA_DIR}/income.csv",
    "expenses": f"{DATA_DIR}/expenses.csv",
    "investments": f"{DATA_DIR}/investments.csv",
    "loans": f"{DATA_DIR}/loans.csv"
}

SCHEMAS = {
    "income": ["Date", "Person", "Type", "Amount"],
    "expenses": ["Date", "Person", "Category", "Amount"],
    "investments": ["Date", "Person", "Instrument", "Amount"],
    "loans": ["Date", "Person", "Loan Type", "Amount", "Status"]
}

# ------------------ FILE INITIALIZATION ------------------
def init_file(file, cols):
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)

for key in FILES:
    init_file(FILES[key], SCHEMAS[key])

# ------------------ LOAD DATA ------------------
income_df = pd.read_csv(FILES["income"])
expense_df = pd.read_csv(FILES["expenses"])
invest_df = pd.read_csv(FILES["investments"])
loan_df = pd.read_csv(FILES["loans"])

# ------------------ SIDEBAR NAV ------------------
menu = st.sidebar.selectbox(
    "Select Section",
    ["Dashboard", "Add Income", "Add Expense", "Add Investment", "Loans"]
)

# ======================================================
# DASHBOARD
# ======================================================
if menu == "Dashboard":
    st.subheader("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Income", f"₹ {income_df['Amount'].sum():,.2f}")
    col2.metric("Total Expenses", f"₹ {expense_df['Amount'].sum():,.2f}")
    col3.metric("Total Investments", f"₹ {invest_df['Amount'].sum():,.2f}")

    active_loans = loan_df[loan_df["Status"] == "Open"]["Amount"].sum()
    col4.metric("Active Loans", f"₹ {active_loans:,.2f}")

    st.divider()

    st.subheader("Person-wise Investments")
    if not invest_df.empty:
        st.bar_chart(invest_df.groupby("Person")["Amount"].sum())

# ======================================================
# ADD INCOME
# ======================================================
elif menu == "Add Income":
    st.subheader("➕ Add Income")

    person = st.selectbox("Person", USERS)
    income_type = st.selectbox("Income Type", ["Salary", "Bonus", "Interest", "Other"])
    amount = st.number_input("Amount", min_value=0.0)
    inc_date = st.date_input("Date", date.today())

    if st.button("Save Income"):
        income_df.loc[len(income_df)] = [inc_date, person, income_type, amount]
        income_df.to_csv(FILES["income"], index=False)
        st.success("Income recorded successfully")

    st.dataframe(income_df)

# ======================================================
# ADD EXPENSE
# ======================================================
elif menu == "Add Expense":
    st.subheader("➖ Add Expense")

    person = st.selectbox("Person", USERS)
    category = st.selectbox(
        "Category",
        ["Food", "Rent", "Travel", "Shopping", "Bills", "Other"]
    )
    amount = st.number_input("Amount", min_value=0.0)
    exp_date = st.date_input("Date", date.today())

    if st.button("Save Expense"):
        expense_df.loc[len(expense_df)] = [exp_date, person, category, amount]
        expense_df.to_csv(FILES["expenses"], index=False)
        st.success("Expense recorded successfully")

    st.dataframe(expense_df)

# ======================================================
# ADD INVESTMENT
# ======================================================
elif menu == "Add Investment":
    st.subheader("📈 Add Investment")

    person = st.selectbox("Person", USERS)
    instrument = st.selectbox(
        "Instrument",
        ["FD", "RD", "Mutual Fund", "Stocks", "PPF", "LIC"]
    )
    amount = st.number_input("Amount", min_value=0.0)
    inv_date = st.date_input("Date", date.today())

    if st.button("Save Investment"):
        invest_df.loc[len(invest_df)] = [inv_date, person, instrument, amount]
        invest_df.to_csv(FILES["investments"], index=False)
        st.success("Investment recorded successfully")

    st.dataframe(invest_df)

# ======================================================
# LOANS
# ======================================================
elif menu == "Loans":
    st.subheader("🤝 Loans (Lent / Borrowed)")

    person = st.selectbox("Person", USERS)
    loan_type = st.selectbox("Loan Type", ["Lent", "Borrowed"])
    amount = st.number_input("Amount", min_value=0.0)
    status = st.selectbox("Status", ["Open", "Closed"])
    loan_date = st.date_input("Date", date.today())

    if st.button("Save Loan Entry"):
        loan_df.loc[len(loan_df)] = [loan_date, person, loan_type, amount, status]
        loan_df.to_csv(FILES["loans"], index=False)
        st.success("Loan entry saved")

    st.dataframe(loan_df)
