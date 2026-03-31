
import streamlit as st
import numpy as np
import math

# 1. 页面基础配置
st.set_page_config(page_title="竞彩全玩法分析器", layout="wide")

st.title("🛡️ 竞彩全玩法 + 泊松模型 终极操盘复合分析器")
st.write("完全按照竞彩官方排版顺序整合：含所有玩法、盈亏数据、泊松分布完整31项比分精算。")

st.divider()

# ================= 第一步：赔率数据录入（按截图顺序） =================
st.header("第一步：录入官方赔率数据")

# ---- 1. 胜平负 ----
st.subheader("【1. 胜平负 赔率】")
col1, col2, col3 = st.columns(3)
win_odd = col1.number_input("胜", 1.0, 1000.0, 1.11, 0.01)
draw_odd = col2.number_input("平", 1.0, 1000.0, 7.10, 0.01)
lose_odd = col3.number_input("负", 1.0, 1000.0, 11.50, 0.01)

# ---- 2. 让球胜平负（动态调节版） ----
st.subheader("【2. 让球 赔率】")
handicap_val = st.number_input("请输入具体让球数 (如让2球填 -2, 受让1球填 1)", min_value=-10, max_value=10, value=-2, step=1)
if handicap_val < 0:
    h_label = f"让球({handicap_val})"
else:
    h_label = f"受让({handicap_val})"

col4, col5, col6 = st.columns(3)
rq_s = col4.number_input(f"{h_label}-胜", 1.0, 1000.0, 2.06, 0.01)
rq_p = col5.number_input(f"{h_label}-平", 1.0, 1000.0, 4.00, 0.01)
rq_f = col6.number_input(f"{h_label}-负", 1.0, 1000.0, 2.54, 0.01)

# ---- 3. 总进球数 ----
st.subheader("【3. 总进球 赔率】")
g_cols1 = st.columns(4)
j_0 = g_cols1[0].number_input("0球", 1.0, 1000.0, 33.00, 0.1)
j_1 = g_cols1[1].number_input("1球", 1.0, 1000.0, 10.00, 0.1)
j_2 = g_cols1[2].number_input("2球", 1.0, 1000.0, 5.30, 0.1)
j_3 = g_cols1[3].number_input("3球", 1.0, 1000.0, 4.10, 0.1)

g_cols2 = st.columns(4)
j_4 = g_cols2[0].number_input("4球", 1.0, 1000.0, 4.00, 0.1)
j_5 = g_cols2[1].number_input("5球", 1.0, 1000.0, 5.60, 0.1)
j_6 = g_cols2[2].number_input("6球", 1.0, 1000.0, 7.75, 0.05)
j_7 = g_cols2[3].number_input("7+球", 1.0, 1000.0, 7.50, 0.1)

# ---- 4. 半全场 ----
st.subheader("【4. 半全场 赔率】")
b_cols1 = st.columns(3)
b_ss = b_cols1[0].number_input("胜胜", 1.0, 1000.0, 1.39, 0.01)
b_sp = b_cols1[1].number_input("胜平", 1.0, 1000.0, 25.00, 0.1)
b_sf = b_cols1[2].number_input("胜负", 1.0, 1000.0, 55.00, 0.1)

b_cols2 = st.columns(3)
b_ps = b_cols2[0].number_input("平胜", 1.0, 1000.0, 4.10, 0.1)
b_pp = b_cols2[1].number_input("平平", 1.0, 1000.0, 13.50, 0.1)
b_pf = b_cols2[2].number_input("平负", 1.0, 1000.0, 30.00, 0.1)

b_cols3 = st.columns(3)
b_fs = b_cols3[0].number_input("负胜", 1.0, 1000.0, 21.00, 0.1)
b_fp = b_cols3[1].number_input("负平", 1.0, 1000.0, 25.00, 0.1)
b_ff = b_cols3[2].number_input("负负", 1.0, 1000.0, 27.00, 0.1)

# ---- 5. 31项全比分 ----
st.subheader("【5. 比分 赔率（含胜/平/负其他）】")

st.markdown("**◆ 主胜比分系列**")
s_cols1 = st.columns(5)
sc_w_other = s_cols1[0].number_input("胜其他", 1.0, 1000.0, 7.60, 0.1)
sc_10 = s_cols1[1].number_input("1:0", 1.0, 1000.0, 10.50, 0.1)
sc_20 = s_cols1[2].number_input("2:0", 1.0, 1000.0, 7.75, 0.05)
sc_21 = s_cols1[3].number_input("2:1", 1.0, 1000.0, 9.50, 0.1)
sc_30 = s_cols1[4].number_input("3:0", 1.0, 1000.0, 6.75, 0.05)

s_cols2 = st.columns(5)
sc_31 = s_cols2[0].number_input("3:1", 1.0, 1000.0, 9.00, 0.1)
sc_32 = s_cols2[1].number_input("3:2", 1.0, 1000.0, 26.00, 0.1)
sc_40 = s_cols2[2].number_input("4:0", 1.0, 1000.0, 9.00, 0.1)
sc_41 = s_cols2[3].number_input("4:1", 1.0, 1000.0, 12.50, 0.1)
sc_42 = s_cols2[4].number_input("4:2", 1.0, 1000.0, 27.00, 0.1)

s_cols3 = st.columns(3)
sc_50 = s_cols3[0].number_input("5:0", 1.0, 1000.0, 13.00, 0.1)
sc_51 = s_cols3[1].number_input("5:1", 1.0, 1000.0, 19.00, 0.1)
sc_52 = s_cols3[2].number_input("5:2", 1.0, 1000.0, 45.00, 0.1)

st.markdown("**◆ 平局比分系列**")
p_cols = st.columns(5)
sc_p_other = p_cols[0].number_input("平其他", 1.0, 1000.0, 175.0, 1.0)
sc_00 = p_cols[1].number_input("0:0", 1.0, 1000.0, 33.00, 0.1)
sc_11 = p_cols[2].number_input("1:1", 1.0, 1000.0, 15.00, 0.1)
sc_22 = p_cols[3].number_input("2:2", 1.0, 1000.0, 23.00, 0.1)
sc_33 = p_cols[4].number_input("3:3", 1.0, 1000.0, 60.00, 0.1)

st.markdown("**◆ 客胜比分系列**")
f_cols1 = st.columns(5)
sc_f_other = f_cols1[0].number_input("负其他", 1.0, 1000.0, 175.0, 1.0)
sc_01 = f_cols1[1].number_input("0:1", 1.0, 1000.0, 45.00, 0.1)
sc_02 = f_cols1[2].number_input("0:2", 1.0, 1000.0, 90.00, 0.1)
sc_12 = f_cols1[3].number_input("1:2", 1.0, 1000.0, 45.00, 0.1)
sc_03 = f_cols1[4].number_input("0:3", 1.0, 1000.0, 200.0, 1.0)

f_cols2 = st.columns(5)
sc_13 = f_cols2[0].number_input("1:3", 1.0, 1000.0, 90.00, 0.1)
sc_23 = f_cols2[1].number_input("2:3", 1.0, 1000.0, 80.00, 0.1)
sc_04 = f_cols2[2].number_input("0:4", 1.0, 1000.0, 450.0, 1.0)
sc_14 = f_cols2[3].number_input("1:4", 1.0, 1000.0, 250.0, 1.0)
sc_24 = f_cols2[4].number_input("2:4", 1.0, 1000.0, 175.0, 1.0)

f_cols3 = st.columns(3)
sc_05 = f_cols3[0].number_input("0:5", 1.0, 1000.0, 750.0, 1.0)
sc_15 = f_cols3[1].number_input("1:5", 1.0, 1000.0, 500.0, 1.0)
sc_25 = f_cols3[2].number_input("2:5", 1.0, 1000.0, 450.0, 1.0)

st.divider()

# ================= 第二步：资金面数据录入 =================
st.header("第二步：录入冷热与资金盈亏面（用于捕捉反向异动）")

# 胜平负资金面
st.subheader("【1. 胜平负 投注与盈亏数据】")
col_z1, col_z2, col_z3 = st.columns(3)
win_bet = col_z1.number_input("主胜 投注比例 (%)", 0.0, 100.0, 60.0, 0.1)
win_prof = col_z1.number_input("主胜 庄家盈亏 (%)", -500.0, 500.0, 33.4, 0.1)

draw_bet = col_z2.number_input("平局 投注比例 (%)", 0.0, 100.0, 17.0, 0.1)
draw_prof = col_z2.number_input("平局 庄家盈亏 (%)", -500.0, 500.0, -20.7, 0.1)

lose_bet = col_z3.number_input("客胜 投注比例 (%)", 0.0, 100.0, 23.0, 0.1)
lose_prof = col_z3.number_input("客胜 庄家盈亏 (%)", -500.0, 500.0, -164.5, 0.1)

# 让球资金面
st.subheader(f"【2. {h_label} 投注与盈亏数据】")
col_zq1, col_zq2, col_zq3 = st.columns(3)
rq_win_bet = col_zq1.number_input(f"{h_label}-胜 投注比例 (%)", 0.0, 100.0, 53.0, 0.1)
rq_win_prof = col_zq1.number_input(f"{h_label}-胜 庄家盈亏 (%)", -500.0, 500.0, -9.18, 0.1)

rq_draw_bet = col_zq2.number_input(f"{h_label}-平 投注比例 (%)", 0.0, 100.0, 27.0, 0.1)
rq_draw_prof = col_zq2.number_input(f"{h_label}-平 庄家盈亏 (%)", -500.0, 500.0, -8.0, 0.1)

rq_lose_bet = col_zq3.number_input(f"{h_label}-负 投注比例 (%)", 0.0, 100.0, 20.0, 0.1)
rq_prof = col_zq3.number_input(f"{h_label}-负 庄家盈亏 (%)", -500.0, 500.0, 49.2, 0.1)

st.divider()

# ================= 第三步：硬核计算区 =================
st.header("第三步：泊松模型独立精算")

col_p1, col_p2 = st.columns(2)
home_lambda = col_p1.number_input("主队预期进球数 (λ1)", 0.1, 10.0, 1.5, 0.1)
away_lambda = col_p2.number_input("客队预期进球数 (λ2)", 0.1, 10.0, 1.2, 0.1)

# 泊松公式
def poisson_prob(lmbda, k):
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

if st.button("🚀 启动复合交叉分析"):
    st.success("分析器启动成功！")
    
    # 构建一个 0 到 6 球的比分概率矩阵 (7x7)
    matrix = np.zeros((7, 7))
    for i in range(7):
        for j in range(7):
            matrix[i][j] = poisson_prob(home_lambda, i) * poisson_prob(away_lambda, j)
            
    # 计算大项总概率
    prob_win = 0.0   # 主胜总概率
    prob_draw = 0.0  # 平局总概率
    prob_lose = 0.0  # 客胜总概率
    
    for i in range(7):
        for j in range(7):
            if i > j:
                prob_win += matrix[i][j]
            elif i == j:
                prob_draw += matrix[i][j]
            else:
                prob_lose += matrix[i][j]
                
    # 计算总进球数(大小球)概率
    prob_under_25 = 0.0  # 小于2.5球
    for i in range(7):
        for j in range(7):
            if (i + j) < 2.5:
                prob_under_25 += matrix[i][j]
    prob_over_25 = 1.0 - prob_under_25  # 大于2.5球

    # 定义31项比分的映射关系
    # 主胜比分系列
    s_scores = {
        "1:0": matrix[1][0], "2:0": matrix[2][0], "2:1": matrix[2][1],
        "3:0": matrix[3][0], "3:1": matrix[3][1], "3:2": matrix[3][2],
        "4:0": matrix[4][0], "4:1": matrix[4][1], "4:2": matrix[4][2],
        "5:0": matrix[5][0], "5:1": matrix[5][1], "5:2": matrix[5][2]
    }
    # 计算【胜其他】
    s_sum_known = sum(s_scores.values())
    s_other = prob_win - s_sum_known
    
    # 平局比分系列
    p_scores = {
        "0:0": matrix[0][0], "1:1": matrix[1][1], "2:2": matrix[2][2], "3:3": matrix[3][3]
    }
    # 计算【平其他】
    p_sum_known = sum(p_scores.values())
    p_other = prob_draw - p_sum_known

    # 客胜比分系列
    f_scores = {
        "0:1": matrix[0][1], "0:2": matrix[0][2], "1:2": matrix[1][2],
        "0:3": matrix[0][3], "1:3": matrix[1][3], "2:3": matrix[2][3],
        "0:4": matrix[0][4], "1:4": matrix[1][4], "2:4": matrix[2][4],
        "0:5": matrix[0][5], "1:5": matrix[1][5], "2:5": matrix[2][5]
    }
    # 计算【负其他】
    f_sum_known = sum(f_scores.values())
    f_other = prob_lose - f_sum_known

    # 1. 输出宏观概率
    st.markdown("### 📊 泊松模型预测结果全景图")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown("**【胜平负大势概率】**")
        st.write(f"* 主胜总概率: `{prob_win*100:.2f}%`")
        st.write(f"* 双方打平总概率: `{prob_draw*100:.2f}%`")
        st.write(f"* 客胜总概率: `{prob_lose*100:.2f}%`")
    with col_res2:
        st.markdown("**【大小球2.5概率】**")
        st.write(f"* 小球（全场总进球 < 2.5）: `{prob_under_25*100:.2f}%`")
        st.write(f"* 大球（全场总进球 > 2.5）: `{prob_over_25*100:.2f}%`")

    st.divider()

    # 2. 输出31项比分明细（完全参照竞彩官方版面排布）
    st.markdown("### 🏆 竞彩官方 31 项比分全维度概率精算")
    
    # 🔴 主胜
    st.markdown("<font color='red'>**🔴 【胜】区比分概率（共13项）**</font>", unsafe_allow_html=True)
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    sc1.metric("胜其他", f"{max(s_other*100, 0.0):.2f}%")
    sc2.metric("1:0", f"{s_scores['1:0']*100:.2f}%")
    sc3.metric("2:0", f"{s_scores['2:0']*100:.2f}%")
    sc4.metric("2:1", f"{s_scores['2:1']*100:.2f}%")
    sc5.metric("3:0", f"{s_scores['3:0']*100:.2f}%")
    
    sc6, sc7, sc8, sc9, sc10 = st.columns(5)
    sc6.metric("3:1", f"{s_scores['3:1']*100:.2f}%")
    sc7.metric("3:2", f"{s_scores['3:2']*100:.2f}%")
    sc8.metric("4:0", f"{s_scores['4:0']*100:.2f}%")
    sc9.metric("4:1", f"{s_scores['4:1']*100:.2f}%")
    sc10.metric("4:2", f"{s_scores['4:2']*100:.2f}%")
    
    sc11, sc12, sc13, _, _ = st.columns(5)
    sc11.metric("5:0", f"{s_scores['5:0']*100:.2f}%")
    sc12.metric("5:1", f"{s_scores['5:1']*100:.2f}%")
    sc13.metric("5:2", f"{s_scores['5:2']*100:.2f}%")
    
    # 🟢 平局
    st.markdown("<font color='green'>**🟢 【平】区比分概率（共5项）**</font>", unsafe_allow_html=True)
    pc1, pc2, pc3, pc4, pc5 = st.columns(5)
    pc1.metric("平其他", f"{max(p_other*100, 0.0):.2f}%")
    pc2.metric("0:0", f"{p_scores['0:0']*100:.2f}%")
    pc3.metric("1:1", f"{p_scores['1:1']*100:.2f}%")
    pc4.metric("2:2", f"{p_scores['2:2']*100:.2f}%")
    pc5.metric("3:3", f"{p_scores['3:3']*100:.2f}%")

    # 🔵 客胜
    st.markdown("<font color='blue'>**🔵 【负】区比分概率（共13项）**</font>", unsafe_allow_html=True)
    fc1, fc2, fc3, fc4, fc5 = st.columns(5)
    fc1.metric("负其他", f"{max(f_other*100, 0.0):.2f}%")
    fc2.metric("0:1", f"{f_scores['0:1']*100:.2f}%")
    fc3.metric("0:2", f"{f_scores['0:2']*100:.2f}%")
    fc4.metric("1:2", f"{f_scores['1:2']*100:.2f}%")
    fc5.metric("0:3", f"{f_scores['0:3']*100:.2f}%")
    
    fc6, fc7, fc8, fc9, fc10 = st.columns(5)
    fc6.metric("1:3", f"{f_scores['1:3']*100:.2f}%")
    fc7.metric("2:3", f"{f_scores['2:3']*100:.2f}%")
    fc8.metric("0:4", f"{f_scores['0:4']*100:.2f}%")
    fc9.metric("1:4", f"{f_scores['1:4']*100:.2f}%")
    fc10.metric("2:4", f"{f_scores['2:4']*100:.2f}%")
    
    fc11, fc12, fc13, _, _ = st.columns(5)
    fc11.metric("0:5", f"{f_scores['0:5']*100:.2f}%")
    fc12.metric("1:5", f"{f_scores['1:5']*100:.2f}%")
    fc13.metric("2:5", f"{f_scores['2:5']*100:.2f}%")

    st.divider()

