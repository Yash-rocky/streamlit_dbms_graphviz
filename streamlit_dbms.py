import streamlit as st
import pandas as pd
import pymysql

# --- Page Configuration ---
st.set_page_config(
    page_title="Advanced Financial Analytics", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished metric styling and custom containers
st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div.block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Database Fetching Function ---
def fetch_data():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",  # Default XAMPP password
            database="sales_db"
        )
        query = "SELECT month, revenue, expenses FROM monthly_sales"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Database Connection Error: {e}")
        return pd.DataFrame()

# Load Data
df_raw = fetch_data()

if not df_raw.empty:
    # --- Data Engineering & Advanced Analytics ---
    df = df_raw.copy()
    df['Profit'] = df['revenue'] - df['expenses']
    # Calculate Profit Margin percentage
    df['Profit Margin (%)'] = round((df['Profit'] / df['revenue']) * 100, 2)
    # Calculate Expense Ratio
    df['Expense Ratio (%)'] = round((df['expenses'] / df['revenue']) * 100, 2)

    # --- Sidebar Filters & Interactions ---
    st.sidebar.header("🕹️ Control Panel")
    st.sidebar.markdown("Use the filters below to adjust the dashboard analytics dynamically.")
    
    # Dynamic Multi-select Filter for Months
    all_months = df['month'].unique()
    selected_months = st.sidebar.multiselect(
        "Filter by Month:",
        options=all_months,
        default=all_months
    )
    
    # Filter the main DataFrame based on user selection
    if selected_months:
        df_filtered = df[df['month'].isin(selected_months)]
    else:
        df_filtered = df.copy()

    # --- Header ---
    st.title("📈 Advanced Financial Performance Dashboard")
    st.subheader("Real-time Analytics from XAMPP Server Architecture")
    st.markdown("---")

    # --- Top KPIs / Metrics Section ---
    total_rev = df_filtered['revenue'].sum()
    total_exp = df_filtered['expenses'].sum()
    total_profit = df_filtered['Profit'].sum()
    avg_margin = df_filtered['Profit Margin (%)'].mean()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Gross Revenue", f"${total_rev:,}")
    m2.metric("Operating Expenses", f"${total_exp:,}")
    # Display net profit with a dynamic target status indicator
    m3.metric("Net Profit", f"${total_profit:,}", delta=f"${int(total_profit * 0.1):,} vs Target")
    m4.metric("Avg Profit Margin", f"{avg_margin:.1f}%")

    st.markdown("### 📊 Visual Analytics")

    # --- Main Charts Layout ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### **Revenue vs Expenses Breakdown**")
        # Unified area chart for clear trend comparisons
        chart_data = df_filtered.set_index('month')[['revenue', 'expenses']]
        st.area_chart(chart_data, height=320)

    with col_right:
        st.markdown("#### **Net Profit Growth Trajectory**")
        # Bar chart with explicit profit mapping
        st.bar_chart(df_filtered.set_index('month')['Profit'], color="#2ecc71", height=320)

    # --- Advanced Analytics Row ---
    st.markdown("---")
    col_table, col_pie = st.columns([3, 2])

    with col_table:
        st.markdown("#### **Detailed Ledger & Margins**")
        # Beautifully formatted data frame with highlighting
        st.dataframe(
            df_filtered.style.background_gradient(subset=['Profit'], cmap='Greens')
                             .background_gradient(subset=['expenses'], cmap='Reds'),
            use_container_width=True
        )
        
        # Feature: Export to CSV button
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Financial Report (CSV)",
            data=csv,
            file_name='financial_report.csv',
            mime='text/csv',
        )

    with col_pie:
        st.markdown("#### **Efficiency Metrics**")
        # Showing a quick text-based trend analysis feature
        st.info("💡 **Operational Insight:**")
        highest_margin_row = df_filtered.loc[df_filtered['Profit Margin (%)'].idxmax()]
        lowest_margin_row = df_filtered.loc[df_filtered['Profit Margin (%)'].idxmin()]
        
        st.write(f"最高 (Highest) efficiency observed in **{highest_margin_row['month']}** with a margin of **{highest_margin_row['Profit Margin (%)']}%**.")
        st.write(f"⚠️ **Attention Needed:** **{lowest_margin_row['month']}** generated the lowest margin performance at **{lowest_margin_row['Profit Margin (%)']}%**.")
        
        # Line chart showing Efficiency Trends
        st.line_chart(df_filtered.set_index('month')['Expense Ratio (%)'], color="#e74c3c")

else:
    st.warning("⚠️ Ready for data. Please ensure XAMPP MySQL is active and the tables contain rows.")