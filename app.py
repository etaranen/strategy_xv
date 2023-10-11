import streamlit as st
import pandas as pd
import numpy as np
 
leaderboard = pd.read_csv("leaderboard.csv")

st.set_page_config(page_title="Midnight Sun Strategy Dashboard", page_icon=":sun:", layout="wide")

# ----- Header Section ---- 

st.title("Midnight Sun Strategy Dashboard")
st.subheader("To easily visualize the members and tickets with the highest velocities over the previous two week sprint")

df = pd.DataFrame(
   np.random.randn(10, 5),
   columns=('col %d' % i for i in range(5)))

st.header("Member Velocity Leaderboard")

st.table(leaderboard)
st.line_chart(leaderboard)

# st.header("Ticket Velocity Leaderboard")

# st.table(df)
# st.line_chart(df)