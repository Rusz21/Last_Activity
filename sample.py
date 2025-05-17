import streamlit as st

import pandas as pd
import numpy as np

import altair as alt

from sqlalchemy import create_engine, inspect
from sqlalchemy import text

warehouse = "postgresql://duckdb_sample_user:i6iKJc6FCs4hVS3AX6yMZngxJvMkzGCs@dpg-d0b2efp5pdvs73c9pi00-a.singapore-postgres.render.com/duckdb_sample"
engine = create_engine(warehouse,  client_encoding='utf8')
connection = engine.connect()

@st.cache_data
def load_data():
    query_ext = """
        SELECT "Product", count(*) AS count
        FROM sales_data_duckdb
        GROUP BY "Product"
        ORDER BY count DESC;
    """
    result = connection.execute(text(query_ext))
    return pd.DataFrame(result.mappings().all())

df = load_data()



st.title("🛒 Sales Dashboard")
st.subheader("📊 Product Sales Overview")

top_n = st.slider("Select number of top products to display", min_value=3, max_value=len(df), value=5)
df_top = df.head(top_n)

chart = alt.Chart(df_top).mark_bar().encode(
    x=alt.X('count:Q', title='Units Sold'),
    y=alt.Y('Product:N', sort='-x', title='Product'),
    tooltip=['Product', 'count']
).properties(
    width=700,
    height=400,
    title="Top Selling Products"
)

st.altair_chart(chart, use_container_width=True)

with st.expander("🔍 View Raw Data"):
    st.dataframe(df, use_container_width=True)



