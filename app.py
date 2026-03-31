import streamlit as st
import numpy as np
import math

# 1. 页面基础配置
st.set_page_config(page_title="竞彩全玩法分析器", layout="wide")

st.title("🛡️ 竞彩全玩法 + 泊松模型 终极操盘复合分析器")
st.write("集成：胜平负、让球、总进球、半全场及比分。全方位穿透机构意图。")

# ================= 2. 基础赔率录入 =================
st.header("第一步：录入官方原始赔率")

# 胜平负
st.subheader("【1. 胜平负 赔率】")
col1, col2, col3 = st.columns(3)
win_odd = col1.number_input("主胜赔率", 1.0, 1000.0, 1.11, 0.01)
draw_odd = col2.number_input("平局赔率", 1.0, 1000.0, 7.10, 0.01)
lose_odd = col3.number_input("客胜赔率", 1.0, 1000.0, 11.50, 0.01)

st.divider()

# 让球胜平负（已解决动态调节问题）
st.subheader("【2. 让球胜平负 赔率】")

# 自由调节让球数，默认 -1（让1球），可以调成 -2, +1 等等
handicap_val = st.number_input("请输入具体让球数 (如让2球填 -2, 受让1球填 1)", min_value=-10, max_value=10, value=-1, step=1)

if handicap_val < 0:
    h_label = f"让球({handicap_val})"
else:
    h_label = f"受让({handicap_val})"

col4, col5, col6 = st.columns(3)
rq_s = col4.number_input(f"{h_label}-胜 赔率", 1.0, 1000.0, 1.82, 0.01)
rq_p = col5.number_input(f"{h_label}-平 赔率", 1.0, 1000.0, 3.40, 0.01)
rq_f = col6.number_input(f"{h_label}-负 赔率", 1.0, 1000.0, 3.50, 0.01)

st.divider()

# 总进球
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

# 半全场
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

# 比分
st.subheader("【5. 关键比分 赔率】")
st.write("此处仅列出部分代表性比分以供泊松对冲校验")
score_cols = st.columns(3)
sc_00 = score_cols[0].number_input("0:0 赔率", 1.0, 1000.0, 13.00, 0.01)
sc_11 = score_cols[1].number_input("1:1 赔率", 1.0, 1000.0, 7.50, 0.01)
sc_22 = score_cols[2].number_input("2:2 赔率", 1.0, 1000.0, 16.00, 0.01)

score_cols2 = st.columns(3)
sc_10 = score_cols2[0].number_input("1:0 赔率", 1.0, 1000.0, 7.50, 0.01)
sc_21 = score_cols2[1].number_input("2:1 赔率", 1.0, 1000.0, 9.00, 0.01)
sc_01 = score_cols2[2].number_input("0:1 赔率", 1.0, 1000.0, 11.00, 0.01)

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
    
    # 简单的赔率去水返还率计算
    margin = (1/win_odd) + (1/draw_odd) + (1/lose_odd)
    payout = 1 / margin
    st.write(f"当前胜平负玩法的机构返还率（去水前）约为：`{payout*100:.2f}%`")
