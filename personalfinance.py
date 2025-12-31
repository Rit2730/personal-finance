import streamlit as st
import pandas as pd
import os
from datetime import date
import math

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Personal Finance Manager", layout="wide")

st.markdown("""
<style>
body { background-color: #0e1117; }
[data-testid="stMetric"] {
    background-color: #161b22;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("Personal Finance Dashboard")
st.caption("Professional personal finance tracking system")

USERS = ["All", "Ritika", "Himanshu", "Seema"]

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "income": "data/income.csv",
    "expenses": "data/expenses.csv",
    "investments": "data/investments.csv",
    "loans": "data/loans.csv"
}

SCHEMAS = {
    "income": ["Date", "Person", "Income Type", "Amount"],
    "expenses": ["Date", "Person", "Category", "Amount"],
    "investments": ["Date", "Person", "Investment Type", "Amount"],
    "loans": ["Date", "Person", "Loan Type", "Amount", "Status"]
}

def init_file(file, cols):
    if not os.path.exists(file):
        pd.DataFrame(columns=cols).to_csv(file, index=False)

for k in FILES:
    init_file(FILES[k], SCHEMAS[k])

income = pd.read_csv(FILES["income"])
expenses = pd.read_csv(FILES["expenses"])
investments = pd.read_csv(FILES["investments"])
loans = pd.read_csv(FILES["loans"])

# ---------------- SIDEBAR ----------------
section = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Income", "Expenses", "Investments", "Loans", "Calculators"]
)

user_filter = st.sidebar.selectbox("Select User", USERS)

def filter_df(df):
    if user_filter == "All":
        return df
    return df[df["Person"] == user_filter]

# ---------------- DASHBOARD ----------------
if section == "Dashboard":
    st.subheader("Overview")

    inc = filter_df(income)
    exp = filter_df(expenses)
    inv = filter_df(investments)
    ln = filter_df(loans)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Income", f"₹ {inc['Amount'].sum():,.0f}")
    c2.metric("Expenses", f"₹ {exp['Amount'].sum():,.0f}")
    c3.metric("Investments", f"₹ {inv['Amount'].sum():,.0f}")
    c4.metric("Active Loans", f"₹ {ln[ln['Status']=='Open']['Amount'].sum():,.0f}")

    st.divider()

    col1, col2 = st.columns(2)

    if not inc.empty:
        col1.subheader("Income Composition")
        col1.pyplot(
            inc.groupby("Income Type")["Amount"].sum().plot.pie(autopct='%1.0f%%').figure
        )

    if not inv.empty:
        col2.subheader("Investment Allocation")
        col2.pyplot(
            inv.groupby("Investment Type")["Amount"].sum().plot.pie(autopct='%1.0f%%').figure
        )

# ---------------- INCOME ----------------
elif section == "Income":
    st.subheader("Add Income")

    person = st.selectbox("Person", USERS[1:])
    itype = st.selectbox("Income Type", ["Salary", "Freelance", "Interest", "Bonus", "Other"])
    amt = st.number_input("Amount", min_value=0.0)
    dt = st.date_input("Date", date.today())

    if st.button("Save Income"):
        income.loc[len(income)] = [dt, person, itype, amt]
        income.to_csv(FILES["income"], index=False)
        st.success("Income added")

    st.dataframe(income)

# ---------------- EXPENSE ----------------
elif section == "Expenses":
    st.subheader("Add Expense")

    person = st.selectbox("Person", USERS[1:])
    cat = st.text_input("Category")
    amt = st.number_input("Amount", min_value=0.0)
    dt = st.date_input("Date", date.today())

    if st.button("Save Expense"):
        expenses.loc[len(expenses)] = [dt, person, cat, amt]
        expenses.to_csv(FILES["expenses"], index=False)
        st.success("Expense added")

    st.dataframe(expenses)

# ---------------- INVESTMENTS ----------------
elif section == "Investments":
    st.subheader("Add Investment")

    person = st.selectbox("Person", USERS[1:])
    inv_type = st.text_input("Investment Type (MF, ETF, FD, PPF, etc)")
    amt = st.number_input("Amount", min_value=0.0)
    dt = st.date_input("Date", date.today())

    if st.button("Save Investment"):
        investments.loc[len(investments)] = [dt, person, inv_type, amt]
        investments.to_csv(FILES["investments"], index=False)
        st.success("Investment added")

    st.dataframe(investments)

# ---------------- LOANS ----------------
elif section == "Loans":
    st.subheader("Loans Tracking")

    person = st.selectbox("Person", USERS[1:])
    ltype = st.selectbox("Loan Type", ["Lent", "Borrowed"])
    amt = st.number_input("Amount", min_value=0.0)
    status = st.selectbox("Status", ["Open", "Closed"])
    dt = st.date_input("Date", date.today())

    if st.button("Save Loan"):
        loans.loc[len(loans)] = [dt, person, ltype, amt, status]
        loans.to_csv(FILES["loans"], index=False)
        st.success("Loan saved")

    st.dataframe(loans)

# ---------------- CALCULATORS ----------------
elif section == "Calculators":
    st.subheader("Investment & Interest Calculators")

    st.markdown("### Compound Interest")
    p = st.number_input("Principal", min_value=0.0)
    r = st.number_input("Rate (%)", min_value=0.0)
    t = st.number_input("Years", min_value=0.0)

    if st.button("Calculate CI"):
        fv = p * ((1 + r/100) ** t)
        st.success(f"Future Value: ₹ {fv:,.2f}")
