import streamlit as st

import pandas as pd
import numpy as np

from sqlalchemy import create_engine, inspect
from sqlalchemy import text

warehouse = "postgresql://duck_test_user:0qrtdjxLyzqwnlKuTlPpUIrqgqaHIkQ4@dpg-d03so9s9c44c7389on60-a.singapore-postgres.render.com/duck_test"
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

