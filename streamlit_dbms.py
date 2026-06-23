import streamlit as st
import pandas as pd
import pymysql

# Set up page config
st.set_page_config(page_title="Company Performance Dashboard", layout="wide")
st.title("📊 Company Financial Dashboard")

# Function to fetch data
def fetch_data():
    conn = pymysql.connect(
        host="localhost", # Note: When hosting on Streamlit Cloud later, this will change to your cloud database credentials!
        user="root",
        password="", #if any error please fill the password (mysql password)here!! 
        database="sales_db"
    )
    query = "SELECT month, revenue, expenses FROM monthly_sales"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Load and visualize the data
try:
    df = fetch_data()
    
    # Data Processing: Calculate profit
    df['profit'] = df['revenue'] - df['expenses']

    # --- Metrics Section ---
    total_rev = df['revenue'].sum()
    total_exp = df['expenses'].sum()
    total_profit = df['profit'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_rev:,}")
    col2.metric("Total Expenses", f"${total_exp:,}")
    col3.metric("Net Profit", f"${total_profit:,}")

    st.markdown("---")

    # --- Charts Section ---
    left_chart_col, right_table_col = st.columns([2, 1])

    with left_chart_col:
        st.subheader("Revenue vs. Expenses Over Time")
        st.line_chart(df.set_index('month')[['revenue', 'expenses']])

        st.subheader("Profit Margin Trend")
        st.bar_chart(df.set_index('month')['profit'])

    with right_table_col:
        st.subheader("Raw Data from MySQL")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Could not connect to the database. Is XAMPP running? Error: {e}")