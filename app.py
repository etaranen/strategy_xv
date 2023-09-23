import streamlit as st
import pandas as pd
import numpy as np
from data_analysis import *

st.set_page_config(page_title="Jira Automation Dashboard", page_icon=":sun:", layout="wide")

# ----- Header Section ---- 

st.subheader("Jira Automation")

st.table(current_data)
st.line_chart(current_data)  
