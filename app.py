
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
st.write("优化版：Dixon-Coles低比分修正 + 智能大球因子 + 纯Python实现")

st.divider()

# ================= 第一步：赔率数据录入（完全保留你的原始代码） =================
st.header("第一步：录入官方赔率数据")

# ---- 1. 胜平负 ----
st.subheader("【1. 胜平负 赔率】")
col1, col2, col3 = st.columns(3)
win_odd = col1.number_input("胜", 1.0, 1000.0, 1.11, 0.01)
draw_odd = col2.number_input("平", 1.0, 1000.0, 7.10, 0.01)
lose_odd = col3.number_input("负", 1.0, 1000.0, 11.50, 0.01)

# ---- 2. 让球胜平负 ----
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
# （以下所有比分输入完全保留你的原始代码，为节省篇幅此处省略，你直接复制粘贴原来的即可）
# ... [把你原来从 st.markdown("**◆ 主胜比分系列**") 到最后一个 sc_25 的所有 number_input 粘贴在这里] ...

st.divider()

# ================= 第二步：资金面数据录入（完全保留） =================
# （同样保留你原来的所有资金面输入代码）

st.divider()

# ================= 第三步：硬核计算区（核心优化部分） =================
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
    rho = st.sidebar.slider("Dixon-Coles ρ (低比分修正)", 0.0, 0.3, 0.10, 0.01)

    # 构建概率矩阵（Dixon-Coles + 8球）
    matrix = np.zeros((9, 9))
    for i in range(9):
        for j in range(9):
            base_prob = poisson_pmf(i, home_lambda_final) * poisson_pmf(j, away_lambda_final)
            # Dixon-Coles 修正
            if i == 0 and j == 0:
                tau = 1 - rho
            elif i == 0 and j == 1 or i == 1 and j == 0:
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

    # ================= 后面的所有代码（31项比分表格、EV、凯利）保持不变 =================
    # （把你原来 if st.button 里面从 “构建一个 0 到 6 球的比分概率矩阵” 之后的所有代码粘贴到这里）

    # 注意：s_scores_raw、p_scores_raw、f_scores_raw 需要把 range(7) 改成 range(9)，其他保持不变

    st.info("✅ 已使用 Dixon-Coles 模型计算，低比分预测更准确！")

# ================= 第五步：凯利准则（使用优化版） =================
# （把你原来的凯利部分替换为我之前优化的版本）

st.divider()
st.header("第五步：凯利准则（Kelly）智能仓位管理")

total_bankroll = st.number_input("操盘总本金（元）", min_value=100, value=10000, step=100)
risk_factor = st.slider("风险系数（建议0.25）", 0.05, 1.0, 0.25, 0.05)

# ...（此处粘贴你原来的 kelly_results 计算代码，我之前优化过的版本也可以）

st.caption("v2.1 优化版 | 在你原代码基础上升级 | 纯Python实现")
