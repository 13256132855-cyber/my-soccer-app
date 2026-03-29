import streamlit as st
import numpy as np

st.set_page_config(page_title="Match Analyzer", layout="centered")

st.title("Full Odds Analyzer")
st.write("Input odds to find anomalies.")
st.divider()

# 1. Home/Draw/Away
with st.expander("1. Match Odds", expanded=True):
    col1, col2, col3 = st.columns(3)
    spf_s = col1.number_input("Home Win", 1.0, 100.0, 2.10, 0.01)
    spf_p = col2.number_input("Draw", 1.0, 100.0, 3.20, 0.01)
    spf_f = col3.number_input("Away Win", 1.0, 100.0, 3.10, 0.01)

# 2. Total Goals
with st.expander("2. Total Goals Odds", expanded=False):
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    g0 = g_col1.number_input("0 Goal", 1.0, 100.0, 9.50, 0.01)
    g1 = g_col2.number_input("1 Goal", 1.0, 100.0, 4.30, 0.01)
    g2 = g_col3.number_input("2 Goals", 1.0, 100.0, 3.30, 0.01)
    g3 = g_col4.number_input("3 Goals", 1.0, 100.0, 3.75, 0.01)
    
    g_col5, g_col6, g_col7, g_col8 = st.columns(4)
    g4 = g_col5.number_input("4 Goals", 1.0, 100.0, 5.40, 0.01)
    g5 = g_col6.number_input("5 Goals", 1.0, 100.0, 9.50, 0.01)
    g6 = g_col7.number_input("6 Goals", 1.0, 100.0, 16.0, 0.1)
    g7 = g_col8.number_input("7+ Goals", 1.0, 100.0, 26.0, 0.1)

# 3. Score
with st.expander("3. Correct Score Odds", expanded=False):
    s_col1, s_col2, s_col3 = st.columns(3)
    s_10 = s_col1.number_input("Score 1:0", 1.0, 100.0, 6.50, 0.01)
    s_00 = s_col2.number_input("Score 0:0", 1.0, 100.0, 9.50, 0.01)
    s_01 = s_col3.number_input("Score 0:1", 1.0, 100.0, 8.50, 0.01)
    
    s_col4, s_col5, s_col6 = st.columns(3)
    s_11 = s_col4.number_input("Score 1:1", 1.0, 100.0, 6.00, 0.01)
    s_21 = s_col5.number_input("Score 2:1", 1.0, 100.0, 8.00, 0.01)
    s_12 = s_col6.number_input("Score 1:2", 1.0, 100.0, 10.0, 0.1)

st.divider()

if st.button("Analyze Now", use_container_width=True):
    st.success("Analysis Complete!")
    
    sum_prob = (1/spf_s) + (1/spf_p) + (1/spf_f)
    payout = round((1 / sum_prob) * 100, 2)
    
    real_s = round(((1/spf_s) / sum_prob) * 100, 2)
    real_p = round(((1/spf_p) / sum_prob) * 100, 2)
    real_f = round(((1/spf_f) / sum_prob) * 100, 2)
    
    st.write("Payout Ratio: " + str(payout) + "%")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Home Prob", str(real_s) + "%")
    c2.metric("Draw Prob", str(real_p) + "%")
    c3.metric("Away Prob", str(real_f) + "%")
    
    st.divider()
    st.subheader("Anomalies Check")
    
    anomalies = 0
    if abs((1/g0) - (1/s_00)) > 0.05:
         st.warning("Warning: 0 Goal odds and Score 0:0 odds have a mathematical gap.")
         anomalies += 1
         
    if anomalies == 0:
        st.info("No obvious anomalies found.")
