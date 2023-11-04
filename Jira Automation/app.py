import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
 
import base64

LOGO_IMAGE = "midsun_logo.png"

st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:50px !important;
        color: #f9a01b !important;
        padding-top: 75px !important;
    }
    .logo-img {
        float:right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text">&nbsp;Midnight Sun Strategy Dashboard</p>
    </div>
    """,
    unsafe_allow_html=True
)


leaderboard = pd.read_csv("leaderboard.csv")

# ----- Subheader Section ---- 

st.subheader("To easily visualize the members and tickets with the highest velocities over the previous two week sprint")


# ----- Leaderboard Section ---- 

df = pd.DataFrame(
   np.random.randn(10, 5),
   columns=('col %d' % i for i in range(5)))
 
st.header("Member Velocity Leaderboard")

st.table(leaderboard)
st.bar_chart(data=leaderboard, x="Name", y="Count",)
