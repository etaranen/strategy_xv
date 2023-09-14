import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Jira Automation Dashboard", page_icon=":sun:", layout="wide")

# ----- Header Section ---- 

st.subheader("Jira Automation")

df = pd.DataFrame(
   np.random.randn(10, 5),
   columns=('col %d' % i for i in range(5)))

st.table(df)
st.line_chart(df)
