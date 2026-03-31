import streamlit as st
import numpy as np
import math

# 1. 页面基础配置
st.set_page_config(page_title="竞彩全玩法分析器", layout="wide")

st.title("🛡️ 竞彩全玩法 + 泊松模型 终极操盘复合分析器")
st.write("集成：胜平负、让球、总进球、半全场及 31 项比分。全方位穿透机构意图。")

# ================= 2. 基础赔率录入 =================
st.header("第一步：录入官方原始赔率与资金面数据")

# ---- 1. 胜平负 & 投注盈亏 ----
st.subheader("【1. 胜平负 赔率与盈亏录入】")
col1, col2, col3 = st.columns(3)

win_odd = col1.number_input("主胜赔率", 1.0, 1000.0, 1.11, 0.01)
win_bet_ratio = col1.number_input("主胜 投注比例 (%)", 0.0, 100.0, 60.0, 0.1)
win_profit = col1.number_input("主胜 庄家盈亏 (%)", -500.0, 500.0, 33.4, 0.1)

draw_odd = col2.number_input("平局赔率", 1.0, 1000.0, 7.10, 0.01)
draw_bet_ratio = col2.number_input("平局 投注比例 (%)", 0.0, 100.0, 17.0, 0.1)
draw_profit = col2.number_input("平局 庄家盈亏 (%)", -500.0, 500.0, -20.7, 0.1)

lose_odd = col3.number_input("客胜赔率", 1.0, 1000.0, 11.50, 0.01)
lose_bet_ratio = col3.number_input("客胜 投注比例 (%)", 0.0, 100.0, 23.0, 0.1)
lose_profit = col3.number_input("客胜 庄家盈亏 (%)", -500.0, 500.0, -164.5, 0.1)

st.divider()

# ---- 2. 让球胜平负（完美动态版） ----
st.subheader("【2. 让球胜平负 赔率与盈亏录入】")

# 自由调节让球数，默认 -2
handicap_val = st.number_input("请输入具体让球数 (如让2球填 -2, 受让1球填 1)", min_value=-10, max_value=10, value=-2, step=1)

if handicap_val < 0:
    h_label = f"让球({handicap_val})"
else:
    h_label = f"受让({handicap_val})"

col4, col5, col6 = st.columns(3)

rq_s = col4.number_input(f"{h_label}-胜 赔率", 1.0, 1000.0, 2.06, 0.01)
rq_win_bet_ratio = col4.number_input(f"{h_label}-胜 投注比 (%)", 0.0, 100.0, 53.0, 0.1)
rq_win_profit = col4.number_input(f"{h_label}-胜 庄家盈亏 (%)", -500.0, 500.0, -9.18, 0.1)

rq_p = col5.number_input(f"{h_label}-平 赔率", 1.0, 1000.0, 4.00, 0.01)
rq_draw_bet_ratio = col5.number_input(f"{h_label}-平 投注比 (%)", 0.0, 100.0, 27.0, 0.1)
rq_draw_profit = col5.number_input(f"{h_label}-平 庄家盈亏 (%)", -500.0, 500.0, -8.0, 0.1)

rq_f = col6.number_input(f"{h_label}-负 赔率", 1.0, 1000.0, 2.54, 0.01)
rq_lose_bet_ratio = col6.number_input(f"{h_label}-负 投注比 (%)", 0.0, 100.0, 20.0, 0.1)
rq_lose_profit = col6.number_input(f"{h_label}-负 庄家盈亏 (%)", -500.0, 500.0, 49.2, 0.1)

st.divider()

# ---- 3. 总进球 ----
st.subheader("【3. 总进球 赔率】")
g_cols = st.columns(4)
j_0 = g_cols[0].number_input("0球", 1.0, 1000.0, 12.00, 0.01)
j_1 = g_cols[1].number_input("1球", 1.0, 1000.0, 5.00, 0.01)
j_2 = g_cols[2].number_input("2球", 1.0, 1000.0, 3.40, 0.01)
j_3 = g_cols[3].number_input("3球", 1.0, 1000.0, 3.80, 0.01)

g_cols2 = st.columns(4)
j_4 = g_cols2[0].number_input("4球", 1.0, 1000.0, 5.80, 0.01)
j_5 = g_cols2[1].number_input("5球", 1.0, 1000.0, 12.00, 0.01)
j_6 = g_cols2[2].number_input("6球", 1.0, 1000.0, 16.00, 0.01)
j_7 = g_cols2[3].number_input("7+球", 1.0, 1000.0, 24.00, 0.01)

st.divider()

# ---- 4. 半全场 ----
st.subheader("【4. 半全场 赔率】")
b_cols1 = st.columns(3)
b_ss = b_cols1[0].number_input("胜胜", 1.0, 1000.0, 6.85, 0.01)
b_sp = b_cols1[1].number_input("胜平", 1.0, 1000.0, 15.00, 0.01)
b_sf = b_cols1[2].number_input("胜负", 1.0, 1000.0, 30.00, 0.01)

b_cols2 = st.columns(3)
b_ps = b_cols2[0].number_input("平胜", 1.0, 1000.0, 4.20, 0.01)
b_pp = b_cols2[1].number_input("平平", 1.0, 1000.0, 5.20, 0.01)
b_pf = b_cols2[2].number_input("平负", 1.0, 1000.0, 8.50, 0.01)

b_cols3 = st.columns(3)
b_fs = b_cols3[0].number_input("负胜", 1.0, 1000.0, 25.00, 0.01)
b_fp = b_cols3[1].number_input("负平", 1.0, 1000.0, 15.00, 0.01)
b_ff = b_cols3[2].number_input("负负", 1.0, 1000.0, 2.30, 0.01)

st.divider()

# ---- 5. 31项比分精细录入 ----
st.subheader("【5. 31项全比分赔率录入】")

# 主胜比分
st.markdown("**◆ 主胜比分**")
s_cols1 = st.columns(5)
sc_10 = s_cols1[0].number_input("1:0", 1.0, 1000.0, 7.50, 0.1)
sc_20 = s_cols1[1].number_input("2:0", 1.0, 1000.0, 8.50, 0.1)
sc_21 = s_cols1[2].number_input("2:1", 1.0, 1000.0, 9.00, 0.1)
sc_30 = s_cols1[3].number_input("3:0", 1.0, 1000.0, 18.00, 0.1)
sc_31 = s_cols1[4].number_input("3:1", 1.0, 1000.0, 19.00, 0.1)

s_cols2 = st.columns(5)
sc_32 = s_cols2[0].number_input("3:2", 1.0, 1000.0, 35.00, 0.1)
sc_40 = s_cols2[1].number_input("4:0", 1.0, 1000.0, 50.00, 0.1)
sc_41 = s_cols2[2].number_input("4:1", 1.0, 1000.0, 50.00, 0.1)
sc_42 = s_cols2[3].number_input("4:2", 1.0, 1000.0, 80.00, 0.1)
sc_50 = s_cols2[4].number_input("5:0", 1.0, 1000.0, 100.0, 0.1)

s_cols3 = st.columns(4)
sc_51 = s_cols3[0].number_input("5:1", 1.0, 1000.0, 120.0, 0.1)
sc_52 = s_cols3[1].number_input("5:2", 1.0, 1000.0, 150.0, 0.1)
sc_w_other = s_cols3[2].number_input("胜其他", 1.0, 1000.0, 40.00, 0.1)

# 平局比分
st.markdown("**◆ 平局比分**")
p_cols = st.columns(5)
sc_00 = p_cols[0].number_input("0:0", 1.0, 1000.0, 13.00, 0.1)
sc_11 = p_cols[1].number_input("1:1", 1.0, 1000.0, 7.50, 0.1)
sc_22 = p_cols[2].number_input("2:2", 1.0, 1000.0, 16.00, 0.1)
sc_33 = p_cols[3].number_input("3:3", 1.0, 1000.0, 60.00, 0.1)
sc_p_other = p_cols[4].number_input("平其他", 1.0, 1000.0, 300.0, 0.1)

# 客胜比分
st.markdown("**◆ 客胜比分**")
f_cols1 = st.columns(5)
sc_01 = f_cols1[0].number_input("0:1", 1.0, 1000.0, 11.00, 0.1)
sc_02 = f_cols1[1].number_input("0:2", 1.0, 1000.0, 15.00, 0.1)
sc_12 = f_cols1[2].number_input("1:2", 1.0, 1000.0, 12.00, 0.1)
sc_03 = f_cols1[3].number_input("0:3", 1.0, 1000.0, 30.00, 0.1)
sc_13 = f_cols1[4].number_input("1:3", 1.0, 1000.0, 28.00, 0.1)

f_cols2 = st.columns(5)
sc_23 = f_cols2[0].number_input("2:3", 1.0, 1000.0, 40.0, 0.1)
sc_04 = f_cols2[1].number_input("0:4", 1.0, 1000.0, 80.0, 0.1)
sc_14 = f_cols2[2].number_input("1:4", 1.0, 1000.0, 80.0, 0.1)
sc_24 = f_cols2[3].number_input("2:4", 1.0, 1000.0, 150.0, 0.1)
sc_05 = f_cols2[4].number_input("0:5", 1.0, 1000.0, 90.0, 0.1)

f_cols3 = st.columns(4)
sc_15 = f_cols3[0].number_input("1:5", 1.0, 1000.0, 80.0, 0.1)
sc_25 = f_cols3[1].number_input("2:5", 1.0, 1000.0, 150.0, 0.1)
sc_f_other = f_cols3[2].number_input("负其他", 1.0, 1000.0, 50.00, 0.1)

st.divider()

# ================= 3. 泊松模型运算 =================
st.header("第二步：泊松硬核数学校验")

col_p1, col_p2 = st.columns(2)
home_lambda = col_p1.number_input("主队预期进球数 (λ1)", 0.1, 10.0, 1.5, 0.1)
away_lambda = col_p2.number_input("客队预期进球数 (λ2)", 0.1, 10.0, 1.2, 0.1)

# 计算泊松分布的函数
def poisson_prob(lmbda, k):
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

if st.button("🚀 启动复合交叉分析"):
    st.success("分析器启动成功！")
    
    # 模拟泊松比分
    p_00 = poisson_prob(home_lambda, 0) * poisson_prob(away_lambda, 0)
    p_11 = poisson_prob(home_lambda, 1) * poisson_prob(away_lambda, 1)
    
    st.markdown("### 📊 泊松模型预测结果")
    st.write(f"根据 λ1={home_lambda} 和 λ2={away_lambda} 的纯数学推算：")
    st.write(f"* 双方打成 **0:0** 的理论概率为：`{p_00*100:.2f}%`")
    st.write(f"* 双方打成 **1:1** 的理论概率为：`{p_11*100:.2f}%`")
    
    st.divider()
    
    # ---- 4大防反杀策略扫描 ----
    st.markdown("### 🛡️ 4大防反杀策略：雷达扫描")
    
    # 策略 1：对称赔率扫描（0球 = 5球 且在 10.00-13.00 之间）
    if abs(j_0 - j_5) <= 0.5 and 10.00 <= j_0 <= 13.00:
        st.error(f"🚨 **【防反杀警报】：触发对称赔率陷阱！**")
        st.markdown(f"  ➔ 发现 `0球` 赔率 **({j_0})** 与 `5球` 赔率 **({j_5})** 形成高度对称！")
    else:
        st.success("🍏 **【防反杀通过】：未发现“0球与5球”的对称赔率陷阱。**")
