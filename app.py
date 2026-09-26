import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Automated Expense Tracker",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Automated Expense Tracker & Analyzer")
st.write("Upload your expense CSV file to analyze your spending.")

uploaded_file = st.file_uploader(
    "Upload a different expense CSV file (optional)",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success("Expense data loaded successfully!")
else:
    default_file = "data/expenses2.csv"

    if os.path.exists(default_file):
        df = pd.read_csv(default_file)
        st.info("Sample expense data loaded automatically.")
    else:
        st.error("Sample data file not found. Please upload a CSV file.")
        st.stop()

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Remove invalid rows
    df = df.dropna(subset=["amount"])

    # Total expense
    total_expense = df["amount"].sum()

    # Average expense
    average_expense = df["amount"].mean()

    # Number of transactions
    transaction_count = len(df)

    st.subheader("📊 Expense Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Expense", f"₹{total_expense:,.2f}")

    with col2:
        st.metric("Average Expense", f"₹{average_expense:,.2f}")

    with col3:
        st.metric("Transactions", transaction_count)

    st.subheader("📋 Transaction Details")

    st.dataframe(df, use_container_width=True)

    # Category analysis
    if "category" in df.columns:

        category_expense = (
            df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.subheader("📌 Category-wise Expense")

        st.dataframe(
            category_expense.reset_index(),
            use_container_width=True
        )

        # Bar chart
        st.subheader("📊 Category-wise Spending")

        st.bar_chart(category_expense)

        # Pie chart
        st.subheader("🥧 Expense Distribution")

        fig, ax = plt.subplots()

        ax.pie(
            category_expense.values,
            labels=category_expense.index,
            autopct="%1.1f%%"
        )

        ax.set_title("Expense Distribution by Category")

        st.pyplot(fig)

    # Account analysis
    if "account" in df.columns:

        account_expense = (
            df.groupby("account")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.subheader("💳 Account-wise Expense")

        st.dataframe(
            account_expense.reset_index(),
            use_container_width=True
        )

    # Highest expense
    highest_expense = df.loc[df["amount"].idxmax()]

    st.subheader("🔎 Highest Expense")

    st.write(
        f"*{highest_expense['description']}* - "
        f"₹{highest_expense['amount']:,.2f}"
    )

    st.success("Analysis completed successfully! 🎉")

