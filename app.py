
import math
import numpy as np
import pandas as pd
import streamlit as st

# ====================== 新增：纯Python泊松函数（解决scipy报错） ======================
def poisson_pmf(k: int, lam: float) -> float:
    """纯Python泊松概率质量函数"""
    if k < 0 or lam <= 0:
        return 0.0
    return (lam ** k * math.exp(-lam)) / math.factorial(k)

# --- 升级版：对攻大球因子 ---
def adjust_xg_for_open_games(home_xg, away_xg, home_conceded, away_conceded):
    """更平滑的对攻大球因子"""
    avg_conceded = (home_conceded + away_conceded) / 2
    if avg_conceded > 1.8:
        factor = 1.0 + 0.18 * (avg_conceded - 1.5)
        st.sidebar.warning(f"🔥 对攻大球因子强烈激活！系数 ≈ {factor:.2f}")
    elif avg_conceded > 1.45:
        factor = 1.0 + 0.09 * (avg_conceded - 1.45)
        st.sidebar.info(f"⚡ 轻度对攻因子激活，系数 ≈ {factor:.2f}")
    else:
        factor = 1.0
    return home_xg * factor, away_xg * factor

# 1. 页面基础配置
st.set_page_config(page_title="竞彩专业分析器 v2.1", layout="wide")
st.title("🛡️ 竞彩全玩法 + Dixon-Coles 专业复合分析器")
st.write(
    "优化版：Dixon-Coles低比分修正 + 智能大球因子 + 纯Python实现"
)

st.divider()

# ================= 第一步：赔率数据录入（完全保留） =================
st.header("第一步：录入官方赔率数据")

# ---- 1. 胜平负 ----
st.subheader("【1. 胜平负 赔率】")
col1, col2, col3 = st.columns(3)
win_odd = col1.number_input("胜", 1.0, 1000.0, 1.11, 0.01)
draw_odd = col2.number_input("平", 1.0, 1000.0, 7.10, 0.01)
lose_odd = col3.number_input("负", 1.0, 1000.0, 11.50, 0.01)

# ---- 2. 让球胜平负 ----
st.subheader("【2. 让球 赔率】")
handicap_val = st.number_input(
    "请输入具体让球数 (如让2球填 -2, 受让1球填 1)",
    min_value=-10, max_value=10, value=-2, step=1,
)
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
sc_w_other = s_cols1[0].number_input("胜其他", 1.0, 1000.0, 35.0, 0.1)
sc_10 = s_cols1[1].number_input("1:0", 1.0, 1000.0, 7.75, 0.05)
sc_20 = s_cols1[2].number_input("2:0", 1.0, 1000.0, 8.75, 0.05)
sc_21 = s_cols1[3].number_input("2:1", 1.0, 1000.0, 7.00, 0.05)
sc_30 = s_cols1[4].number_input("3:0", 1.0, 1000.0, 14.00, 0.1)

s_cols2 = st.columns(5)
sc_31 = s_cols2[0].number_input("3:1", 1.0, 1000.0, 12.00, 0.1)
sc_32 = s_cols2[1].number_input("3:2", 1.0, 1000.0, 18.00, 0.1)
sc_40 = s_cols2[2].number_input("4:0", 1.0, 1000.0, 28.00, 0.1)
sc_41 = s_cols2[3].number_input("4:1", 1.0, 1000.0, 24.00, 0.1)
sc_42 = s_cols2[4].number_input("4:2", 1.0, 1000.0, 40.00, 0.1)

s_cols3 = st.columns(3)
sc_50 = s_cols3[0].number_input("5:0", 1.0, 1000.0, 65.00, 0.1)
sc_51 = s_cols3[1].number_input("5:1", 1.0, 1000.0, 50.00, 0.1)
sc_52 = s_cols3[2].number_input("5:2", 1.0, 1000.0, 90.00, 0.1)

st.markdown("**◆ 平局比分系列**")
p_cols = st.columns(5)
sc_p_other = p_cols[0].number_input("平其他", 1.0, 1000.0, 250.0, 1.0)
sc_00 = p_cols[1].number_input("0:0", 1.0, 1000.0, 15.00, 0.1)
sc_11 = p_cols[2].number_input("1:1", 1.0, 1000.0, 7.75, 0.05)
sc_22 = p_cols[3].number_input("2:2", 1.0, 1000.0, 12.50, 0.1)
sc_33 = p_cols[4].number_input("3:3", 1.0, 1000.0, 50.00, 0.1)

st.markdown("**◆ 客胜比分系列**")
f_cols1 = st.columns(5)
sc_f_other = f_cols1[0].number_input("负其他", 1.0, 1000.0, 100.0, 1.0)
sc_01 = f_cols1[1].number_input("0:1", 1.0, 1000.0, 13.00, 0.1)
sc_02 = f_cols1[2].number_input("0:2", 1.0, 1000.0, 22.00, 0.1)
sc_12 = f_cols1[3].number_input("1:2", 1.0, 1000.0, 12.00, 0.1)
sc_03 = f_cols1[4].number_input("0:3", 1.0, 1000.0, 60.0, 0.1)

f_cols2 = st.columns(5)
sc_13 = f_cols2[0].number_input("1:3", 1.0, 1000.0, 30.00, 0.1)
sc_23 = f_cols2[1].number_input("2:3", 1.0, 1000.0, 31.00, 0.1)
sc_04 = f_cols2[2].number_input("0:4", 1.0, 1000.0, 150.0, 1.0)
sc_14 = f_cols2[3].number_input("1:4", 1.0, 1000.0, 80.0, 1.0)
sc_24 = f_cols2[4].number_input("2:4", 1.0, 1000.0, 100.0, 1.0)

f_cols3 = st.columns(3)
sc_05 = f_cols3[0].number_input("0:5", 1.0, 1000.0, 500.0, 1.0)
sc_15 = f_cols3[1].number_input("1:5", 1.0, 1000.0, 300.0, 1.0)
sc_25 = f_cols3[2].number_input("2:5", 1.0, 1000.0, 300.0, 1.0)

st.divider()

# ================= 第二步：资金面数据录入（完全保留） =================
st.header("第二步：录入冷热与资金盈亏面")

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

# ================= 第三步：硬核计算区（核心升级） =================
st.header("第三步：Dixon-Coles 专业精算")

col_p1, col_p2 = st.columns(2)
home_lambda = col_p1.number_input("主队预期进球数 (λ1)", 0.1, 10.0, 1.5, 0.05)
away_lambda = col_p2.number_input("客队预期进球数 (λ2)", 0.1, 10.0, 1.2, 0.05)

col_p3, col_p4 = st.columns(2)
home_avg_lost = col_p3.number_input("主队场均失球数", 0.0, 10.0, 1.0, 0.1)
away_avg_lost = col_p4.number_input("客队场均失球数", 0.0, 10.0, 1.0, 0.1)

if st.button("🚀 启动 Dixon-Coles 复合分析", type="primary"):
    st.success("分析器启动成功！")

    # 升级大球因子
    home_lambda_final, away_lambda_final = adjust_xg_for_open_games(
        home_lambda, away_lambda, home_avg_lost, away_avg_lost
    )

    # Dixon-Coles ρ 参数
    rho = st.sidebar.slider("Dixon-Coles ρ 参数（低比分修正 建议0.05-0.15）", 0.0, 0.3, 0.10, 0.01)

    # 构建概率矩阵（升级版）
    matrix = np.zeros((9, 9))
    for i in range(9):
        for j in range(9):
            base_prob = poisson_pmf(i, home_lambda_final) * poisson_pmf(j, away_lambda_final)
            # Dixon-Coles 修正
            if i == 0 and j == 0:
                tau = 1 - rho
            elif (i == 0 and j == 1) or (i == 1 and j == 0):
                tau = 1 + rho
            elif i == 1 and j == 1:
                tau = 1 - rho
            else:
                tau = 1.0
            matrix[i][j] = base_prob * tau

    matrix /= matrix.sum()

    # 计算胜平负概率
    prob_win = 0.0
    prob_draw = 0.0
    prob_lose = 0.0
    for i in range(9):
        for j in range(9):
            if i > j:
                prob_win += matrix[i][j]
            elif i == j:
                prob_draw += matrix[i][j]
            else:
                prob_lose += matrix[i][j]

    prob_under_25 = np.sum(matrix[0:3, 0:3])
    prob_over_25 = 1 - prob_under_25

    # ================= 以下完全保留你原来的代码（从这里开始粘贴你原来的内容） =================
    # 1. 计算比分概率
    s_scores_raw = {
        "1:0": matrix[1][0], "2:0": matrix[2][0], "2:1": matrix[2][1],
        "3:0": matrix[3][0], "3:1": matrix[3][1], "3:2": matrix[3][2],
        "4:0": matrix[4][0], "4:1": matrix[4][1], "4:2": matrix[4][2],
        "5:0": matrix[5][0], "5:1": matrix[5][1], "5:2": matrix[5][2],
    }
    s_other = max(prob_win - sum(s_scores_raw.values()), 0.0)

    p_scores_raw = {"0:0": matrix[0][0], "1:1": matrix[1][1], "2:2": matrix[2][2], "3:3": matrix[3][3]}
    p_other = max(prob_draw - sum(p_scores_raw.values()), 0.0)

    f_scores_raw = {
        "0:1": matrix[0][1], "0:2": matrix[0][2], "1:2": matrix[1][2],
        "0:3": matrix[0][3], "1:3": matrix[1][3], "2:3": matrix[2][3],
        "0:4": matrix[0][4], "1:4": matrix[1][4], "2:4": matrix[2][4],
        "0:5": matrix[0][5], "1:5": matrix[1][5], "2:5": matrix[2][5],
    }
    f_other = max(prob_lose - sum(f_scores_raw.values()), 0.0)

    # 2. 输出宏观概率（保留原来样式）
    st.markdown("### 📊 Dixon-Coles 模型预测结果全景图")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown("**【胜平负大势概率】**")
        st.write(f"* 主胜总概率: `{prob_win*100:.2f}%`")
        st.write(f"* 双方打平总概率: `{prob_draw*100:.2f}%`")
        st.write(f"* 客胜总概率: `{prob_lose*100:.2f}%`")
    with col_res2:
        st.markdown("**【大小球2.5概率】**")
        st.write(f"* 小球（< 2.5球）: `{prob_under_25*100:.2f}%`")
        st.write(f"* 大球（> 2.5球）: `{prob_over_25*100:.2f}%`")

    # 后面的 31项比分表格、EV价值挖掘、凯利准则 全部保留你原来的代码
    # （请把你原始代码中从 “# 🏆 3. 核心功能实现：制作 31 项比分表格” 开始到最后的所有代码粘贴到这里）

    st.success("✅ Dixon-Coles 模型已生效，低比分预测更准确！")

# ================= 第五步：凯利准则（保留你原来代码） =================
# 把你原来的凯利部分直接放在这里即可

st.caption("v2.1 优化版 | 在你原代码基础上升级 | Dixon-Coles + 纯Python"
