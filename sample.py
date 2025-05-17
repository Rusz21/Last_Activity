import streamlit as st

import pandas as pd
import numpy as np

import altair as alt

from sqlalchemy import create_engine, inspect
from sqlalchemy import text

warehouse = "postgresql://duckdb_sample_user:i6iKJc6FCs4hVS3AX6yMZngxJvMkzGCs@dpg-d0b2efp5pdvs73c9pi00-a.singapore-postgres.render.com/duckdb_sample"
engine = create_engine(warehouse,  client_encoding='utf8')
connection = engine.connect()

@st.cache_data(ttl=600)
def load_data():
    query = """
        SELECT "Order Date", "Product", "Price Each", "Quantity Ordered"
        FROM sales_data_duckdb
        WHERE "Order Date" IS NOT NULL
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        df = pd.DataFrame(result.mappings().all())
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Revenue'] = df['Price Each'] * df['Quantity Ordered']
        return df

df = load_data()

# Filter by date
st.sidebar.header("📅 Filter by Date")
min_date, max_date = df['Order Date'].min(), df['Order Date'].max()
date_range = st.sidebar.date_input("Select date range", [min_date, max_date], min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    df = df[(df['Order Date'] >= pd.to_datetime(date_range[0])) & (df['Order Date'] <= pd.to_datetime(date_range[1]))]

# Grouped Data
product_sales = df.groupby("Product", as_index=False).agg({
    "Quantity Ordered": "sum",
    "Revenue": "sum"
}).sort_values("Quantity Ordered", ascending=False)

# Title
st.title("🛒 Sales Dashboard")
st.markdown("### 🔥 Product Performance Overview")

# --- Most Bought Products Chart
top_n = st.slider("Show Top N Products by Units Sold", 3, len(product_sales), 10)
top_products = product_sales.head(top_n)

bar_chart = alt.Chart(top_products).mark_bar().encode(
    x=alt.X('Quantity Ordered:Q', title='Units Sold'),
    y=alt.Y('Product:N', sort='-x', title='Product'),
    tooltip=['Product', 'Quantity Ordered', 'Revenue']
).properties(title="Top Selling Products", width=700)

st.altair_chart(bar_chart, use_container_width=True)

# --- Pie Chart for Market Share
st.markdown("### 🥧 Product Market Share")
pie_data = top_products.copy()
pie_data['Share'] = pie_data['Quantity Ordered'] / pie_data['Quantity Ordered'].sum()

pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Share", type="quantitative"),
    color=alt.Color(field="Product", type="nominal"),
    tooltip=['Product', alt.Tooltip('Share:Q', format='.2%')]
).properties(width=500, height=400)

st.altair_chart(pie_chart, use_container_width=False)

# --- Time-Series Line Chart
st.markdown("### 📈 Sales Over Time")
df_daily = df.groupby(df['Order Date'].dt.to_period('D')).agg({
    'Quantity Ordered': 'sum',
    'Revenue': 'sum'
}).reset_index()
df_daily['Order Date'] = df_daily['Order Date'].dt.to_timestamp()

line_chart = alt.Chart(df_daily).mark_line().encode(
    x='Order Date:T',
    y='Revenue:Q',
    tooltip=['Order Date', 'Revenue']
).properties(title="Daily Revenue Trend", width=750)

st.altair_chart(line_chart, use_container_width=True)

# --- Raw Data Table
with st.expander("🔍 Full Sales Data"):
    st.dataframe(df, use_container_width=True)




