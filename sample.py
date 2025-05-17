import streamlit as st

import pandas as pd
import numpy as np

from sqlalchemy import create_engine, inspect
from sqlalchemy import text

warehouse = "postgresql://duckdb_sample_user:i6iKJc6FCs4hVS3AX6yMZngxJvMkzGCs@dpg-d0b2efp5pdvs73c9pi00-a.singapore-postgres.render.com/duckdb_sample"
engine = create_engine(warehouse,  client_encoding='utf8')
connection = engine.connect()

@st.cache_data
def load_data(query):  # Added query parameter
    """
    Executes a SQL query and returns the result as a Pandas DataFrame.
    """
    result = connection.execute(text(query))
    df = pd.DataFrame(result.mappings().all())
    return df

# --- New Section: Display Table Structure ---
st.title("Sales Data Overview")
st.subheader("First 5 Rows of sales_data_duckdb")

# Fetch and display the first 5 rows
query_table_preview = "SELECT * FROM sales_data_duckdb LIMIT 5;"
df_preview = load_data(query_table_preview)  # Use the load_data function
st.dataframe(df_preview)  # Use st.dataframe for better display

# --- Original Section: Bar Chart ---
st.subheader("Most bought product") #Moved Subheader here for better flow
# Fetch and display the product counts
query_product_counts = """
SELECT "Product", count(*) AS count
FROM sales_data_duckdb
GROUP BY "Product";
"""
df_product_counts = load_data(query_product_counts)
st.bar_chart(df_product_counts.set_index('Product'))

connection.close()




