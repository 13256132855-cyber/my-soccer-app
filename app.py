import streamlit as st
import numpy as np

st.set_page_config(page_title="Jingcai Full Odds Analyzer", layout="wide")

st.title("Jingcai Full Odds Analyzer v2.0")
st.write("Input all 5 categories of odds to find anomalies.")
st.divider()

# 1. 胜平负 / 让球胜平负
with st.expander("📊 1. 胜平负 / 让球 赔率录入", expanded=True):
    col1, col2, col3 = st.columns(3)
    spf_s = col1.number_input("胜 (Home Win)", 1.0, 1000.0, 3.92, 0.01)
    spf_p = col2.number_input("平 (Draw)", 1.0, 1000.0, 3.30, 0.01)
    spf_f = col3.number_input("负 (Away Win)", 1.0, 1000.0, 1.75, 0.01)
    
    st.write("让球盘口 (+1 / -1 等)")
    col4, col5, col6 = st.columns(3)
    rq_s = col4.number_input("让胜 (Handicap Home)", 1.0, 1000.0, 1.82, 0.01)
    rq_p = col5.number_input("让平 (Handicap Draw)", 1.0, 1000.0, 3.40, 0.01)
    rq_f = col6.number_input("让负 (Handicap Away)", 1.0, 1000.0, 3.50, 0.01)

# 2. 总进球数 (0-7+球)
with st.expander("⚽ 2. 总进球数赔率录入", expanded=False):
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    g0 = g_col1.number_input("0 球", 1.0, 1000.0, 12.00, 0.01)
    g1 = g_col2.number_input("1 球", 1.0, 1000.0, 4.75, 0.01)
    g2 = g_col3.number_input("2 球", 1.0, 1000.0, 3.45, 0.01)
    g3 = g_col4.number_input("3 球", 1.0, 1000.0, 3.60, 0.01)
    
    g_col5, g_col6, g_col7, g_col8 = st.columns(4)
    g4 = g_col5.number_input("4 球", 1.0, 1000.0, 5.50, 0.01)
    g5 = g_col6.number_input("5 球", 1.0, 1000.0, 9.50, 0.01)
    g6 = g_col7.number_input("6 球", 1.0, 1000.0, 16.00, 0.01)
    g7 = g_col8.number_input("7+ 球", 1.0, 1000.0, 24.00, 0.01)

# 3. 半全场 (9项)
with st.expander("⏳ 3. 半全场赔率录入", expanded=False):
    b_col1, b_col2, b_col3 = st.columns(3)
    b_ss = b_col1.number_input("胜胜 (W/W)", 1.0, 1000.0, 6.85, 0.01)
    b_sp = b_col2.number_input("胜平 (W/D)", 1.0, 1000.0, 15.00, 0.01)
    b_sf = b_col3.number_input("胜负 (W/L)", 1.0, 1000.0, 25.00, 0.01)
    
    b_col4, b_col5, b_col6 = st.columns(3)
    b_ps = b_col4.number_input("平胜 (D/W)", 1.0, 1000.0, 8.50, 0.01)
    b_pp = b_col5.number_input("平平 (D/D)", 1.0, 1000.0, 5.30, 0.01)
    b_pf = b_col6.number_input("平负 (D/L)", 1.0, 1000.0, 4.30, 0.01)
    
    b_col7, b_col8, b_col9 = st.columns(3)
    b_fs = b_col7.number_input("负胜 (L/W)", 1.0, 1000.0, 40.00, 0.01)
    b_fp = b_col8.number_input("负平 (L/D)", 1.0, 1000.0, 15.00, 0.01)
    b_ff = b_col9.number_input("负负 (L/L)", 1.0, 1000.0, 2.70, 0.01)

# 4. 比分 (31项)
with st.expander("🏁 4. 正确比分赔率录入", expanded=False):
    # 主胜比分
    st.write("【主胜比分】")
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    s_10 = sc1.number_input("1:0", 1.0, 1000.0, 11.0, 0.1)
    s_20 = sc2.number_input("2:0", 1.0, 1000.0, 22.0, 0.1)
    s_21 = sc3.number_input("2:1", 1.0, 1000.0, 12.0, 0.1)
    s_30 = sc4.number_input("3:0", 1.0, 1000.0, 55.0, 0.1)
    s_31 = sc5.number_input("3:1", 1.0, 1000.0, 32.0, 0.1)
    
    sc6, sc7, sc8, sc9, sc10 = st.columns(5)
    s_32 = sc6.number_input("3:2", 1.0, 1000.0, 36.0, 0.1)
    s_40 = sc7.number_input("4:0", 1.0, 1000.0, 175.0, 0.1)
    s_41 = sc8.number_input("4:1", 1.0, 1000.0, 120.0, 0.1)
    s_42 = sc9.number_input("4:2", 1.0, 1000.0, 120.0, 0.1)
    s_50 = sc10.number_input("5:0", 1.0, 1000.0, 550.0, 0.1)
    
    sc11, sc12, sc13, sc14 = st.columns(4)
    s_51 = sc11.number_input("5:1", 1.0, 1000.0, 350.0, 0.1)
    s_52 = sc12.number_input("5:2", 1.0, 1000.0, 450.0, 0.1)
    s_swin_other = sc13.number_input("胜其他", 1.0, 1000.0, 120.0, 0.1)
    
    # 平局比分
    st.write("【平局比分】")
    sc15, sc16, sc17, sc18, sc19 = st.columns(5)
    s_00 = sc15.number_input("0:0", 1.0, 1000.0, 12.0, 0.1)
    s_11 = sc16.number_input("1:1", 1.0, 1000.0, 6.3, 0.1)
    s_22 = sc17.number_input("2:2", 1.0, 1000.0, 14.0, 0.1)
    s_33 = sc18.number_input("3:3", 1.0, 1000.0, 60.0, 0.1)
    s_draw_other = sc19.number_input("平其他", 1.0, 1000.0, 250.0, 0.1)
    
    # 客胜比分
    st.write("【客胜比分】")
    sc20, sc21, sc22, sc23, sc24 = st.columns(5)
    s_01 = sc20.number_input("0:1", 1.0, 1000.0, 7.0, 0.1)
    s_02 = sc21.number_input("0:2", 1.0, 1000.0, 8.0, 0.1)
    s_12 = sc22.number_input("1:2", 1.0, 1000.0, 7.0, 0.1)
    s_03 = sc23.number_input("0:3", 1.0, 1000.0, 15.0, 0.1)
    s_13 = sc24.number_input("1:3", 1.0, 1000.0, 12.0, 0.1)
    
    sc25, sc26, sc27, sc28, sc29 = st.columns(5)
    s_23 = sc25.number_input("2:3", 1.0, 1000.0, 22.0, 0.1)
    s_04 = sc26.number_input("0:4", 1.0, 1000.0, 31.0, 0.1)
    s_14 = sc27.number_input("1:4", 1.0, 1000.0, 30.0, 0.1)
    s_24 = sc28.number_input("2:4", 1.0, 1000.0, 55.0, 0.1)
    s_05 = sc29.number_input("0:5", 1.0, 1000.0, 90.0, 0.1)
    
    sc30, sc31, sc32 = st.columns(3)
    s_15 = sc30.number_input("1:5", 1.0, 1000.0, 80.0, 0.1)
    s_25 = sc31.number_input("2:5", 1.0, 1000.0, 150.0, 0.1)
    s_lose_other = sc32.number_input("负其他", 1.0, 1000.0, 50.0, 0.1)

st.divider()

if st.button("立即分析全赔率 (Analyze)", use_container_width=True):
    st.success("数据载入成功！(Data Loaded)")
    
    # 计算返还率
    sum_prob = (1/spf_s) + (1/spf_p) + (1/spf_f)
    payout = round((1 / sum_prob) * 100, 2)
    
    # 真实概率
    real_s = round(((1/spf_s) / sum_prob) * 100, 2)
    real_p = round(((1/spf_p) / sum_prob) * 100, 2)
    real_f = round(((1/spf_f) / sum_prob) * 100, 2)
    
    st.subheader("📊 竞彩返还率与真实概率")
    st.write(f"该场比赛竞彩返还率约为: **{payout}%**")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("主胜真实率 (Home Prob)", f"{real_s}%")
    c2.metric("平局真实率 (Draw Prob)", f"{real_p}%")
    c3.metric("客胜真实率 (Away Prob)", f"{real_f}%")
    
    st.divider()
    
    # 交叉验证逻辑
    st.subheader("🛡️ 异常坐标初步筛查 (Anomalies Check)")
    anomalies = 0
    
    # 逻辑1：0球与比分0:0的概率冲突
    prob_0g = 1 / g0
    prob_00sc = 1 / s_00
    if abs(prob_0g - prob_00sc) > 0.03:
        st.warning("⚠️ 警告：总进球数0球 与 比分0:0 的赔率存在数学剪刀差，机构必有一边在诱导。")
        anomalies += 1
        
    # 逻辑2：总进球大球偏向和比分的冲突
    prob_big = (1/g3) + (1/g4) + (1/g5) + (1/g6) + (1/g7)
    if prob_big > 0.6 and (s_10 < 7.0 or s_01 < 7.0):
        st.warning("⚠️ 警告：总进球严重倾向3球及以上，但 1:0 或 0:1 小比分赔率被打压得很低，存在诱导小比分可能。")
        anomalies += 1
        
    if anomalies == 0:
        st.info("✅ 暂未在核心录入赔率中发现明显逻辑冲突。")
