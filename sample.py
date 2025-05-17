import streamlit as st

import pandas as pd
import numpy as np

from sqlalchemy import create_engine, inspect
from sqlalchemy import text

warehouse = "postgresql://duckdb_sample_user:i6iKJc6FCs4hVS3AX6yMZngxJvMkzGCs@dpg-d0b2efp5pdvs73c9pi00-a.singapore-postgres.render.com/duckdb_sample"
engine = create_engine(warehouse,  client_encoding='utf8')
connection = engine.connect()

@st.cache_data
def load_data():
    query_ext = """
        SELECT "Product", count(*) AS count
        FROM all_data
        GROUP BY "Product";
    """
    result = connection.execute(text(query_ext))
    return pd.DataFrame(result.mappings().all())

df = load_data()



st.title("Sales Dashboard")
st.subheader("Most bought product")
st.bar_chart(df.set_index('Product'))

