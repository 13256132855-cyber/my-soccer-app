import streamlit as st
import numpy as np
import math
import pandas as pd  # 导入 Pandas 用于制作精美表格
import matplotlib.pyplot as plt

# 1. 页面基础配置
st.set_page_config(page_title="竞彩全玩法分析器", layout="wide")
# ================= 第一步：基本面六维雷达图 =================
st.header("第一步：双队基本面战力雷达")
st.write("📊 请根据两队近期表现（积分、近况、交锋、防守、进攻、控球）进行打分（1-10分）。")

# 1. 创建两列用于输入两队的六维数据
col_r1, col_r2 = st.columns(2)

with col_r1:
    st.markdown("**🏠 主队能力值**")
    h_points = st.slider("主队积分/排名实力", 1.0, 10.0, 7.0, 0.5)
    h_form = st.slider("主队近期胜率/状态", 1.0, 10.0, 6.5, 0.5)
    h_h2h = st.slider("主队历史交锋心理", 1.0, 10.0, 5.0, 0.5)
    h_def = st.slider("主队防守零封能力", 1.0, 10.0, 8.0, 0.5)
    h_att = st.slider("主队进攻爆破能力", 1.0, 10.0, 6.0, 0.5)
    h_poss = st.slider("主队控球场面传控", 1.0, 10.0, 7.5, 0.5)

with col_r2:
    st.markdown("**🤖 客队能力值**")
    a_points = st.slider("客队积分/排名实力", 1.0, 10.0, 8.0, 0.5)
    a_form = st.slider("客队近期胜率/状态", 1.0, 10.0, 7.5, 0.5)
    a_h2h = st.slider("客队历史交锋心理", 1.0, 10.0, 5.0, 0.5)
    a_def = st.slider("客队防守零封能力", 1.0, 10.0, 6.0, 0.5)
    a_att = st.slider("客队进攻爆破能力", 1.0, 10.0, 8.5, 0.5)
    a_poss = st.slider("客队控球场面传控", 1.0, 10.0, 6.5, 0.5)

# 2. Matplotlib 雷达图绘制逻辑
categories = ['积分实力', '近期胜率', '交锋心理', '防守能力', '进攻能力', '控球传控']
N = len(categories)

# 旋转角度
angles = [n / float(N) * 2 * math.pi for n in range(N)]
angles += angles[:1] # 闭合图形

# 组装数据
home_values = [h_points, h_form, h_h2h, h_def, h_att, h_poss]
home_values += home_values[:1]

away_values = [a_points, a_form, a_h2h, a_def, a_att, a_poss]
away_values += away_values[:1]

# 开始画图
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans'] # 优先中文字体
plt.rcParams['axes.unicode_minus'] = False 

# 画主队
ax.plot(angles, home_values, linewidth=2, linestyle='solid', label='主队', color='#FF4B4B')
ax.fill(angles, home_values, '#FF4B4B', alpha=0.25)

# 画客队
ax.plot(angles, away_values, linewidth=2, linestyle='solid', label='客队', color='#0068C9')
ax.fill(angles, away_values, '#0068C9', alpha=0.25)

# 添加刻度和标签
plt.xticks(angles[:-1], categories, size=10)
ax.set_rlabel_position(0)
plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="grey", size=8)
plt.ylim(0, 10)

plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

# 在Streamlit中显示图片
st.pyplot(fig)
st.divider()


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

    # 1. 计算比分概率
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

    # 🏆 3. 核心功能实现：制作 31 项比分表格（概率在下，字体变小）
    st.markdown("### 🏆 竞彩官方 31 项比分全维度概率精算（高亮高概率）")
    
    # 辅助函数：根据概率大小生成背景色的CSS
    def get_color(prob, max_prob, base_color):
        if max_prob == 0:
            return ""
        # 按照当前格子的概率占最高概率的比例，分配透明度(0.1 ~ 0.8)
        alpha = 0.1 + 0.7 * (prob / max_prob)
        if base_color == "red":
            return f"background-color: rgba(255, 0, 0, {alpha});"
        elif base_color == "green":
            return f"background-color: rgba(0, 128, 0, {alpha});"
        elif base_color == "blue":
            return f"background-color: rgba(0, 0, 255, {alpha});"
        return ""

    # 🔴 【胜】区表格
    st.markdown("<font color='red' size='4'>**🔴 【胜】区比分概率（共13项）**</font>", unsafe_allow_html=True)
    s_labels = ["胜其他", "1:0", "2:0", "2:1", "3:0", "3:1", "3:2", "4:0", "4:1", "4:2", "5:0", "5:1", "5:2"]
    s_vals = [s_other, s_scores_raw["1:0"], s_scores_raw["2:0"], s_scores_raw["2:1"], s_scores_raw["3:0"], s_scores_raw["3:1"], s_scores_raw["3:2"], s_scores_raw["4:0"], s_scores_raw["4:1"], s_scores_raw["4:2"], s_scores_raw["5:0"], s_scores_raw["5:1"], s_scores_raw["5:2"]]
    
    max_s = max(s_vals) if s_vals else 1.0
    s_html = "<div style='overflow-x:auto;'><table style='width:100%; text-align:center; border-collapse:collapse; font-size:12px; border:1px solid #ddd;'>"
    s_html += "<tr>" + "".join([f"<th style='border:1px solid #ddd; padding:4px; background-color:#f9f9f9;'>{lbl}</th>" for lbl in s_labels]) + "</tr>"
    s_html += "<tr>" + "".join([f"<td style='border:1px solid #ddd; padding:4px; {get_color(v, max_s, 'red')}'>{v*100:.2f}%</td>" for v in s_vals]) + "</tr>"
    s_html += "</table></div>"
    st.markdown(s_html, unsafe_allow_html=True)

    # 🟢 【平】区表格
    st.markdown("<br><font color='green' size='4'>**🟢 【平】区比分概率（共5项）**</font>", unsafe_allow_html=True)
    p_labels = ["平其他", "0:0", "1:1", "2:2", "3:3"]
    p_vals = [p_other, p_scores_raw["0:0"], p_scores_raw["1:1"], p_scores_raw["2:2"], p_scores_raw["3:3"]]
    
    max_p = max(p_vals) if p_vals else 1.0
    p_html = "<div style='overflow-x:auto;'><table style='width:100%; text-align:center; border-collapse:collapse; font-size:12px; border:1px solid #ddd;'>"
    p_html += "<tr>" + "".join([f"<th style='border:1px solid #ddd; padding:4px; background-color:#f9f9f9;'>{lbl}</th>" for lbl in p_labels]) + "</tr>"
    p_html += "<tr>" + "".join([f"<td style='border:1px solid #ddd; padding:4px; {get_color(v, max_p, 'green')}'>{v*100:.2f}%</td>" for v in p_vals]) + "</tr>"
    p_html += "</table></div>"
    st.markdown(p_html, unsafe_allow_html=True)

    # 🔵 【负】区表格
    st.markdown("<br><font color='blue' size='4'>**🔵 【负】区比分概率（共13项）**</font>", unsafe_allow_html=True)
    f_labels = ["负其他", "0:1", "0:2", "1:2", "0:3", "1:3", "2:3", "0:4", "1:4", "2:4", "0:5", "1:5", "2:5"]
    f_vals = [f_other, f_scores_raw["0:1"], f_scores_raw["0:2"], f_scores_raw["1:2"], f_scores_raw["0:3"], f_scores_raw["1:3"], f_scores_raw["2:3"], f_scores_raw["0:4"], f_scores_raw["1:4"], f_scores_raw["2:4"], f_scores_raw["0:5"], f_scores_raw["1:5"], f_scores_raw["2:5"]]
    
    max_f = max(f_vals) if f_vals else 1.0
    f_html = "<div style='overflow-x:auto;'><table style='width:100%; text-align:center; border-collapse:collapse; font-size:12px; border:1px solid #ddd;'>"
    f_html += "<tr>" + "".join([f"<th style='border:1px solid #ddd; padding:4px; background-color:#f9f9f9;'>{lbl}</th>" for lbl in f_labels]) + "</tr>"
    f_html += "<tr>" + "".join([f"<td style='border:1px solid #ddd; padding:4px; {get_color(v, max_f, 'blue')}'>{v*100:.2f}%</td>" for v in f_vals]) + "</tr>"
    f_html += "</table></div>"
    st.markdown(f_html, unsafe_allow_html=True)

    st.divider()

    # ================= 第四步：机构级期望值（Value Bet）挖掘模块 =================
    st.divider()
    st.header("第四步：博弈期望值（Value Bet）深度挖掘")
    st.write("💡 庄家视角：寻找【真实概率 × 官方赔率 > 1】的数学漏洞。")

    # 1. 计算胜平负的机构抽水与隐含概率
    # 隐含概率 = 1 / 赔率
    implied_win = 1 / win_odd
    implied_draw = 1 / draw_odd
    implied_lose = 1 / lose_odd
    total_implied = implied_win + implied_draw + implied_lose
    
    # 算出官方在这场比赛胜平负玩法的抽水（返还率 = 1 / total_implied）
    return_rate = (1 / total_implied) * 100
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown("**【市场隐含概率 vs 你的泊松概率】**")
        st.write(f"* 官方测定主胜概率: `{implied_win/total_implied*100:.2f}%` (你算出: `{prob_win*100:.2f}%`)")
        st.write(f"* 官方测定平局概率: `{implied_draw/total_implied*100:.2f}%` (你算出: `{prob_draw*100:.2f}%`)")
        st.write(f"* 官方测定客胜概率: `{implied_lose/total_implied*100:.2f}%` (你算出: `{prob_lose*100:.2f}%`)")
    with col_v2:
        st.markdown("**【机构风控指标】**")
        st.write(f"* 本场官方原始抽水（Overround）: `{(total_implied - 1)*100:.2f}%`")
        st.write(f"* 理论返还率（Payout）: `{return_rate:.2f}%`")

    # 2. 计算期望值 (Value = 泊松概率 * 官方赔率)
    ev_win = prob_win * win_odd
    ev_draw = prob_draw * draw_odd
    ev_lose = prob_lose * lose_odd

    st.markdown("### 🎯 胜平负玩法期望值（EV）")
    st.write("注：EV > 1.00 说明该选项赔率被机构低估，具备长期投注的“正期望值”价值。")
    
    # 制作胜平负期望值表格
    ev_data = {
        "玩法选项": ["主胜 (3)", "平局 (1)", "客胜 (0)"],
        "官方赔率": [win_odd, draw_odd, lose_odd],
        "你的理论概率": [f"{prob_win*100:.2f}%", f"{prob_draw*100:.2f}%", f"{prob_lose*100:.2f}%"],
        "期望值 (EV)": [round(ev_win, 3), round(ev_draw, 3), round(ev_lose, 3)]
    }
    ev_df = pd.DataFrame(ev_data)
    
    # 用颜色高亮EV > 1.0 的行
    def highlight_ev(row):
        return ['background-color: rgba(0, 128, 0, 0.2)' if row['期望值 (EV)'] > 1.0 else '' for _ in row]
    
    st.dataframe(ev_df.style.apply(highlight_ev, axis=1), use_container_width=True)

    # 3. 进阶：比分玩法的极限捡漏（找出Top 3高价值比分）
    st.markdown("### 💎 31项比分高价值捡漏雷达")
    
    all_scores = []
    # 整合胜区
    for lbl, prob in zip(s_labels, s_vals):
        all_scores.append({"比分": lbl, "概率": prob, "赔率": globals().get(f"sc_{lbl.replace(':', '')}") if lbl != "胜其他" else sc_w_other})
    # 整合平区
    for lbl, prob in zip(p_labels, p_vals):
        all_scores.append({"比分": lbl, "概率": prob, "赔率": globals().get(f"sc_{lbl.replace(':', '')}") if lbl != "平其他" else sc_p_other})
    # 整合负区
    for lbl, prob in zip(f_labels, f_vals):
        all_scores.append({"比分": lbl, "概率": prob, "赔率": globals().get(f"sc_{lbl.replace(':', '')}") if lbl != "负其他" else sc_f_other})
        
    # 计算每个比分的EV
    for item in all_scores:
        if item["赔率"] is not None:
            item["期望值 (EV)"] = round(item["概率"] * item["赔率"], 3)
        else:
            item["期望值 (EV)"] = 0.0

    # 排序，找出EV最高的比分
    sorted_scores = sorted(all_scores, key=lambda x: x["期望值 (EV)"], reverse=True)
    
    top_n = 3
    st.write(f"根据您的泊松输入，本场 EV 最高的 **前 {top_n} 个** 捡漏比分如下：")
    
    for i in range(min(top_n, len(sorted_scores))):
        best = sorted_scores[i]
        if best["期望值 (EV)"] > 1.0:
            st.success(f"🔥 排名第 {i+1}：比分 **{best['比分']}** | 概率: `{best['概率']*100:.2f}%` | 赔率: `{best['赔率']}` | **EV: {best['期望值 (EV)']}** (极具博取价值！)")
        else:
            st.warning(f"ℹ️ 排名第 {i+1}：比分 **{best['比分']}** | 概率: `{best['概率']*100:.2f}%` | 赔率: `{best['赔率']}` | **EV: {best['期望值 (EV)']}** (暂未发现绝对数学漏洞)")
# ================= 第五步：凯利准则智能仓位控制 =================
st.divider()
st.header("第五步：凯利准则（Kelly）智能仓位管理")
st.write("💰 模型将根据上面扫出的“正期望值”比分，自动计算出最科学的资金分配比例。")

# 1. 设定总本金
total_bankroll = st.number_input("请输入你的操盘总本金（元）：", min_value=100, value=10000, step=100)
risk_factor = st.slider("操盘风险系数（建议使用 0.25 即四分之一凯利，更稳健）", 0.05, 1.0, 0.25, 0.05)

st.markdown("### 🎯 推荐投注仓位（仅展示 EV > 1.0 且仓位 > 0 的捡漏选项）")

kelly_results = []

# 直接复用你代码里的 all_scores 变量
for item in all_scores:
    prob = item.get("概率", 0)
    odds = item.get("赔率", 0)
    label = item.get("比分", "未知")
    
    if odds and odds > 1: # 赔率必须大于1才有意义
        # 计算凯利百分比
        p = prob / 100.0  # 转为小数概率
        b = odds - 1.0
        q = 1.0 - p
        
        kelly_percent = (p * b - q) / b if b > 0 else 0
        
        # 计算 EV
        ev = p * odds
        
        # 只有当 EV > 1 且凯利算出来的仓位大于 0 时才推荐
        if ev > 1.00 and kelly_percent > 0:
            adjusted_kelly = kelly_percent * risk_factor  # 乘以风险系数（分注）
            bet_money = total_bankroll * adjusted_kelly
            
            kelly_results.append({
                "比分": label,
                "期望值(EV)": round(ev, 3),
                "理论概率": f"{prob}%",
                "官方赔率": odds,
                "建议仓位": f"{round(adjusted_kelly * 100, 2)}%",
                "建议投注金额": f"{round(bet_money, 2)} 元"
            })

# 3. 输出表格
if kelly_results:
    import pandas as pd
    # 按照期望值从大到小排序
    df_kelly = pd.DataFrame(kelly_results)
    st.dataframe(df_kelly.sort_values(by="期望值(EV)", ascending=False), use_container_width=True)
    st.success("💡 策略提示：凯利公式是基于大数定律的数学最优解，切勿重仓梭哈，严格按照分注（如1/4凯利）执行方能复利增长！")
else:
    st.warning("🔍 当前输入的数据中，没有发现具备“正期望值”且符合凯利法则的捡漏比分。")


