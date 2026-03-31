
import streamlit as st
import numpy as np
import math
import pandas as pd  # 导入 Pandas 用于制作精美表格

# 1. 页面基础配置
st.set_page_config(page_title="竞彩全玩法分析器", layout="wide")

st.title("🛡️ 竞彩全玩法 + 泊松模型 终极操盘复合分析器")
st.write("完全按照竞彩官方排版顺序整合：含所有玩法、盈亏数据、泊松分布完整31项比分精算（含热力图大表）。")

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
            
    # 计算胜平负总概率
    prob_win = 0.0   # 主胜总概率
    prob_draw = 0.0  # 平局总概率
    prob_lose = 0.0  # 客胜总概率
    for i in range(7):
        for j in range(7):
            if i > j: prob_win += matrix[i][j]
            elif i == j: prob_draw += matrix[i][j]
            else: prob_lose += matrix[i][j]
                
    # 计算大小球2.5概率
    prob_under_25 = 0.0
    for i in range(7):
        for j in range(7):
            if (i + j) < 2.5: prob_under_25 += matrix[i][j]
    prob_over_25 = 1.0 - prob_under_25

    # 1. 定义31项比分的映射关系并计算概率
    s_scores_raw = {
        "1:0": matrix[1][0], "2:0": matrix[2][0], "2:1": matrix[2][1],
        "3:0": matrix[3][0], "3:1": matrix[3][1], "3:2": matrix[3][2],
        "4:0": matrix[4][0], "4:1": matrix[4][1], "4:2": matrix[4][2],
        "5:0": matrix[5][0], "5:1": matrix[5][1], "5:2": matrix[5][2]
    }
    s_other = max(prob_win - sum(s_scores_raw.values()), 0.0)
    
    p_scores_raw = {
        "0:0": matrix[0][0], "1:1": matrix[1][1], "2:2": matrix[2][2], "3:3": matrix[3][3]
    }
    p_other = max(prob_draw - sum(p_scores_raw.values()), 0.0)

    f_scores_raw = {
        "0:1": matrix[0][1], "0:2": matrix[0][2], "1:2": matrix[1][2],
        "0:3": matrix[0][3], "1:3": matrix[1][3], "2:3": matrix[2][3],
        "0:4": matrix[0][4], "1:4": matrix[1][4], "2:4": matrix[2][4],
        "0:5": matrix[0][5], "1:5": matrix[1][5], "2:5": matrix[2][5]
    }
    f_other = max(prob_lose - sum(f_scores_raw.values()), 0.0)

    # 2. 输出宏观概率
    st.markdown("### 📊 泊松模型预测结果全景图")
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

    st.divider()

    # 🏆 3. 核心功能实现：制作 31 项比分热力表格（字变小，概率在下，高亮高概率）
    st.markdown("### 🏆 竞彩官方 31 项比分全维度概率精算（颜色高亮热力图）")
    
    # 🔴 【胜】区表格
    st.markdown("<font color='red' size='4'>**🔴 【胜】区比分概率（共13项）**</font>", unsafe_allow_html=True)
    # 整合数据为 DataFrame
    s_data = {
        "比分": ["胜其他", "1:0", "2:0", "2:1", "3:0", "3:1", "3:2", "4:0", "4:1", "4:2", "5:0", "5:1", "5:2"],
        "概率": [s_other, s_scores_raw["1:0"], s_scores_raw["2:0"], s_scores_raw["2:1"], s_scores_raw["3:0"], s_scores_raw["3:1"], s_scores_raw["3:2"], s_scores_raw["4:0"], s_scores_raw["4:1"], s_scores_raw["4:2"], s_scores_raw["5:0"], s_scores_raw["5:1"], s_scores_raw["5:2"]]
    }
    df_s = pd.DataFrame(s_data)
    # 转置表格，让比分在首行，概率在下
    df_s_T = df_s.set_index("比分").T
    
    # 🟢 【平】区表格
    st.markdown("<font color='green' size='4'>**🟢 【平】区比分概率（共5项）**</font>", unsafe_allow_html=True)
    p_data = {
        "比分": ["平其他", "0:0", "1:1", "2:2", "3:3"],
        "概率": [p_other, p_scores_raw["0:0"], p_scores_raw["1:1"], p_scores_raw["2:2"], p_scores_raw["3:3"]]
    }
    df_p = pd.DataFrame(p_data)
    df_p_T = df_p.set_index("比分").T

    # 🔵 【负】区表格
    st.markdown("<font color='blue' size='4'>**🔵 【负】区比分概率（共13项）**</font>", unsafe_allow_html=True)
    f_data = {
        "比分": ["负其他", "0:1", "0:2", "1:2", "0:3", "1:3", "2:3", "0:4", "1:4", "2:4", "0:5", "1:5", "2:5"],
        "概率": [f_other, f_scores_raw["0:1"], f_scores_raw["0:2"], f_scores_raw["1:2"], f_scores_raw["0:3"], f_scores_raw["1:3"], f_scores_raw["2:3"], f_scores_raw["0:4"], f_scores_raw["1:4"], f_scores_raw["2:4"], f_scores_raw["0:5"], f_scores_raw["1:5"], f_scores_raw["2:5"]]
    }
    df_f = pd.DataFrame(f_data)
    df_f_T = df_f.set_index("比分").T

    # 定义一个内部函数，用于生成和渲染表格（含颜色和字体优化）
    def render_hot_table(df_T, color_cmap):
        # 1. 格式化：转为百分比
        formatted_df = df_T.applymap(lambda x: f"{x*100:.2f}%")
        
        # 2. 颜色风格：使用 Pandas Styler 生成颜色
        styled_df = formatted_df.style.background_gradient(
            axis=1,            # 按行应用颜色
            vmin=0.0,          # 颜色刻度起点为 0
            vmax=df_T.values.max(), # 颜色刻度终点为当前表格最大概率
            cmap=color_cmap,   # 颜色风格（胜区用Reds，平区用Greens，负区用Blues）
            gmap=df_T.values   # **关键：颜色深浅依据原始概率值计算，而非格式化后的字符串**
        ).set_properties(**{
            'font-size': '12px',    # **字体变小 (默认是14px或16px)**
            'text-align': 'center' # 居中对齐
        })
        
        # 3. 在 Streamlit 中显示
        st.dataframe(styled_df, use_container_width=True)

    # 渲染三个区的表格
    # 使用 st.cache_data 来避免重复渲染以提高速度
    render_hot_table(df_s_T, 'Reds')   # 胜区用红色热力图
    render_hot_table(df_p_T, 'Greens') # 平区用绿色热力图
    render_hot_table(df_f_T, 'Blues')  # 负区用蓝色热力图

    st.divider()

