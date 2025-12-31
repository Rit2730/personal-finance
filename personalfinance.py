import streamlit as st
import pandas as pd
import os
from datetime import date
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Manager", layout="wide")

st.title("Personal Finance Dashboard")
st.caption("Professional personal finance system")

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

def init_file(path, cols):
    if not os.path.exists(path):
        pd.DataFrame(columns=cols).to_csv(path, index=False)

for k in FILES:
    init_file(FILES[k], SCHEMAS[k])

income = pd.read_csv(FILES["income"])
expenses = pd.read_csv(FILES["expenses"])
investments = pd.read_csv(FILES["investments"])
loans = pd.read_csv(FILES["loans"])

st.sidebar.title("Navigation")
section = st.sidebar.selectbox(
    "Section",
    ["Dashboard", "Income", "Expenses", "Investments", "Loans", "Calculators"]
)
user = st.sidebar.selectbox("User", USERS)

def f(df):
    return df if user == "All" else df[df["Person"] == user]

# ================= DASHBOARD =================
if section == "Dashboard":
    inc, exp, inv, ln = f(income), f(expenses), f(investments), f(loans)

    net_worth = (
        inc["Amount"].sum()
        - exp["Amount"].sum()
        + inv["Amount"].sum()
        + ln[(ln["Loan Type"]=="Lent") & (ln["Status"]=="Open")]["Amount"].sum()
        - ln[(ln["Loan Type"]=="Borrowed") & (ln["Status"]=="Open")]["Amount"].sum()
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Income", f"₹ {inc['Amount'].sum():,.0f}")
    c2.metric("Expenses", f"₹ {exp['Amount'].sum():,.0f}")
    c3.metric("Investments", f"₹ {inv['Amount'].sum():,.0f}")
    c4.metric("Net Worth", f"₹ {net_worth:,.0f}")

    st.divider()

    col1, col2 = st.columns(2)

    if not inc.empty:
        col1.subheader("Income Composition")
        fig, ax = plt.subplots()
        inc.groupby("Income Type")["Amount"].sum().plot.pie(
            autopct="%1.0f%%", ax=ax
        )
        ax.set_ylabel("")
        col1.pyplot(fig)

    if not inv.empty:
        col2.subheader("Investment Allocation")
        fig, ax = plt.subplots()
        inv.groupby("Investment Type")["Amount"].sum().plot.pie(
            autopct="%1.0f%%", ax=ax
        )
        ax.set_ylabel("")
        col2.pyplot(fig)

# ================= INCOME =================
elif section == "Income":
    st.subheader("Add Income")

    p = st.selectbox("Person", USERS[1:])
    t = st.selectbox("Income Type", ["Salary","Freelance","Interest","Bonus","Other"])
    a = st.number_input("Amount", min_value=0.0)
    d = st.date_input("Date", date.today())

    if st.button("Save"):
        income.loc[len(income)] = [d,p,t,a]
        income.to_csv(FILES["income"], index=False)
        st.success("Income saved")

    st.dataframe(income)

# ================= EXPENSE =================
elif section == "Expenses":
    st.subheader("Add Expense")

    p = st.selectbox("Person", USERS[1:])
    c = st.text_input("Category")
    a = st.number_input("Amount", min_value=0.0)
    d = st.date_input("Date", date.today())

    if st.button("Save"):
        expenses.loc[len(expenses)] = [d,p,c,a]
        expenses.to_csv(FILES["expenses"], index=False)
        st.success("Expense saved")

    st.dataframe(expenses)

# ================= INVESTMENTS =================
elif section == "Investments":
    st.subheader("Add Investment")

    p = st.selectbox("Person", USERS[1:])
    i = st.text_input("Investment Type (MF, ETF, FD, PPF, etc)")
    a = st.number_input("Amount", min_value=0.0)
    d = st.date_input("Date", date.today())

    if st.button("Save"):
        investments.loc[len(investments)] = [d,p,i,a]
        investments.to_csv(FILES["investments"], index=False)
        st.success("Investment saved")

    st.dataframe(investments)

# ================= LOANS =================
elif section == "Loans":
    st.subheader("Loans")

    p = st.selectbox("Person", USERS[1:])
    t = st.selectbox("Type", ["Lent","Borrowed"])
    a = st.number_input("Amount", min_value=0.0)
    s = st.selectbox("Status", ["Open","Closed"])
    d = st.date_input("Date", date.today())

    if st.button("Save"):
        loans.loc[len(loans)] = [d,p,t,a,s]
        loans.to_csv(FILES["loans"], index=False)
        st.success("Loan saved")

    st.dataframe(loans)

# ================= CALCULATORS =================
elif section == "Calculators":
    st.subheader("Interest Calculators")

    p = st.number_input("Principal", min_value=0.0)
    r = st.number_input("Rate (%)", min_value=0.0)
    t = st.number_input("Years", min_value=0.0)

    if st.button("Compound Interest"):
        fv = p * ((1 + r/100) ** t)
        st.success(f"Future Value: ₹ {fv:,.2f}")
