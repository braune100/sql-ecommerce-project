import streamlit as st
import pandas as pd
import sqlite3

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="E-commerce Analytics Dashboard", layout="wide")

st.title("E-commerce Analytics Dashboard")
st.markdown(
    """
This dashboard analyzes e-commerce transactions using **SQL, Python, Pandas, and Streamlit**.
It provides insights into revenue trends, customer behavior, and product performance.
"""
)

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
@st.cache_resource
def get_connection():
    return sqlite3.connect("ecommerce.db", check_same_thread=False)

conn = get_connection()

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM ecommerce"
    df = pd.read_sql_query(query, conn)
    return df

df = load_data()

# ---------------------------
# CLEAN DATA
# ---------------------------
df.columns = df.columns.str.lower().str.strip()

# Convert numeric columns safely
if "quantity" in df.columns:
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

if "unitprice" in df.columns:
    df["unitprice"] = pd.to_numeric(df["unitprice"], errors="coerce")

# Convert date safely
if "invoicedate" in df.columns:
    df["invoicedate"] = pd.to_datetime(df["invoicedate"], errors="coerce")

# Drop rows missing important values
required_cols = []
if "quantity" in df.columns:
    required_cols.append("quantity")
if "unitprice" in df.columns:
    required_cols.append("unitprice")

if required_cols:
    df = df.dropna(subset=required_cols)

# Create revenue column
if "quantity" in df.columns and "unitprice" in df.columns:
    df["revenue"] = df["quantity"] * df["unitprice"]

# Create month column
if "invoicedate" in df.columns:
    df["month"] = df["invoicedate"].dt.to_period("M").astype(str)

# Safety check
if "revenue" not in df.columns:
    st.error("Revenue column could not be created. Check your column names in the database.")
    st.write("Current columns:", df.columns.tolist())
    st.stop()

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("Filters")

filtered_df = df.copy()

# Country filter
if "country" in df.columns:
    country_options = ["All"] + sorted(df["country"].dropna().astype(str).unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", country_options)

    if selected_country != "All":
        filtered_df = filtered_df[filtered_df["country"] == selected_country]

# Date filter
if "invoicedate" in df.columns and not df["invoicedate"].isna().all():
    min_date = df["invoicedate"].min().date()
    max_date = df["invoicedate"].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["invoicedate"].dt.date >= start_date) &
            (filtered_df["invoicedate"].dt.date <= end_date)
        ]

# ---------------------------
# KPI METRICS
# ---------------------------
total_orders = filtered_df["invoiceno"].nunique() if "invoiceno" in filtered_df.columns else len(filtered_df)
total_revenue = filtered_df["revenue"].sum()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Avg Order Value", f"${avg_order_value:,.2f}")

# ---------------------------
# SALES BY MONTH
# ---------------------------
st.subheader("Sales by Month")

if "month" in filtered_df.columns and not filtered_df.empty:
    monthly_sales = (
        filtered_df.groupby("month")["revenue"]
        .sum()
        .reset_index()
        .sort_values("month")
    )
    st.line_chart(monthly_sales.set_index("month"))

# ---------------------------
# TOP PRODUCTS
# ---------------------------
st.subheader("Top Products")

if "description" in filtered_df.columns and not filtered_df.empty:
    top_products = (
        filtered_df.groupby("description")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_products)

# ---------------------------
# TOP CUSTOMERS
# ---------------------------
st.subheader("Top Customers")

if "customerid" in filtered_df.columns and not filtered_df.empty:
    top_customers = (
        filtered_df.dropna(subset=["customerid"])
        .groupby("customerid")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_customers)

# ---------------------------
# SALES BY COUNTRY
# ---------------------------
st.subheader("Sales by Country")

if "country" in filtered_df.columns and not filtered_df.empty:
    country_sales = (
        filtered_df.groupby("country")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(country_sales)

# ---------------------------
# DATA PREVIEW
# ---------------------------
st.subheader("Data Preview")
st.dataframe(filtered_df.head(20))