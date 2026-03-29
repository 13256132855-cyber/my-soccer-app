import streamlit as st
import numpy as np
import math

st.set_page_config(page_title="竞彩全能操盘分析器", layout="wide")

st.title("🛡️ 竞彩全玩法 + 泊松模型 终极操盘复合分析器")
st.write("已集成：胜平负、让球、总进球、半全场及31项比分。全方位穿透机构意图。")
st.divider()

# ================= 1. 泊松分布纯算法 =================
def get_poisson(k, lamb):
    if lamb <= 0:
        return 0.0
    return (math.pow(lamb, k) * math.exp(-lamb)) / math.factorial(k)

st.sidebar.header("📊 泊松模型：预期进球设定")
home_exp = st.sidebar.slider("主队预期进球数", 0.1, 5.0, 1.5, 0.05)
away_exp = st.sidebar.slider("客队预期进球数", 0.1, 5.0, 1.2, 0.05)

# ================= 2. 基础赔率录入 =================
with st.expander("📊 1. 胜平负 & 让球胜平负", expanded=True):
    st.write("【基础 胜平负 赔率】")
    col1, col2, col3 = st.columns(3)
    spf_s = col1.number_input("胜 (Home Win)", 1.0, 1000.0, 3.92, 0.01)
    spf_p = col2.number_input("平 (Draw)", 1.0, 1000.0, 3.30, 0.01)
    spf_f = col3.number_input("负 (Away Win)", 1.0, 1000.0, 1.75, 0.01)
    
    st.write("【让球胜平负 (+1 或 -1)】")
    col4, col5, col6 = st.columns(3)
    rq_s = col4.number_input("让球-胜", 1.0, 1000.0, 1.82, 0.01)
    rq_p = col5.number_input("让球-平", 1.0, 1000.0, 3.40, 0.01)
    rq_f = col6.number_input("让球-负", 1.0, 1000.0, 3.50, 0.01)

with st.expander("⚽ 2. 总进球数 赔率录入", expanded=True):
    tc1, tc2, tc3, tc4 = st.columns(4)
    j_0 = tc1.number_input("0球", 1.0, 1000.0, 12.0, 0.1)
    j_1 = tc2.number_input("1球", 1.0, 1000.0, 4.75, 0.1)
    j_2 = tc3.number_input("2球", 1.0, 1000.0, 3.45, 0.1)
    j_3 = tc4.number_input("3球", 1.0, 1000.0, 3.60, 0.1)
    
    tc5, tc6, tc7, tc8 = st.columns(4)
    j_4 = tc5.number_input("4球", 1.0, 1000.0, 5.50, 0.1)
    j_5 = tc6.number_input("5球", 1.0, 1000.0, 9.50, 0.1)
    j_6 = tc7.number_input("6球", 1.0, 1000.0, 16.0, 0.1)
    j_7 = tc8.number_input("7+球", 1.0, 1000.0, 24.0, 0.1)

with st.expander("🌓 3. 半全场 赔率录入", expanded=True):
    bc1, bc2, bc3 = st.columns(3)
    bq_ss = bc1.number_input("胜胜", 1.0, 1000.0, 6.85, 0.01)
    bq_sp = bc2.number_input("胜平", 1.0, 1000.0, 15.0, 0.01)
    bq_sf = bc3.number_input("胜负", 1.0, 1000.0, 25.0, 0.01)
    
    bc4, bc5, bc6 = st.columns(3)
    bq_ps = bc4.number_input("平胜", 1.0, 1000.0, 8.50, 0.01)
    bq_pp = bc5.number_input("平平", 1.0, 1000.0, 5.30, 0.01)
    bq_pf = bc6.number_input("平负", 1.0, 1000.0, 4.30, 0.01)
    
    bc7, bc8, bc9 = st.columns(3)
    bq_fs = bc7.number_input("负胜", 1.0, 1000.0, 40.0, 0.01)
    bq_fp = bc8.number_input("负平", 1.0, 1000.0, 15.0, 0.01)
    bq_ff = bc9.number_input("负负", 1.0, 1000.0, 2.70, 0.01)

with st.expander("🏁 4. 竞彩比分赔率录入 (31项)", expanded=True):
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
    
    sc11, sc12, sc13 = st.columns(3)
    s_51 = sc11.number_input("5:1", 1.0, 1000.0, 350.0, 0.1)
    s_52 = sc12.number_input("5:2", 1.0, 1000.0, 450.0, 0.1)
    s_swin_other = sc13.number_input("胜其他", 1.0, 1000.0, 120.0, 0.1)
    
    st.write("【平局比分】")
    sc15, sc16, sc17, sc18, sc19 = st.columns(5)
    s_00 = sc15.number_input("0:0", 1.0, 1000.0, 12.0, 0.1)
    s_11 = sc16.number_input("1:1", 1.0, 1000.0, 6.3, 0.1)
    s_22 = sc17.number_input("2:2", 1.0, 1000.0, 14.0, 0.1)
    s_33 = sc18.number_input("3:3", 1.0, 1000.0, 60.0, 0.1)
    s_draw_other = sc19.number_input("平其他", 1.0, 1000.0, 250.0, 0.1)
    
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

# ================= 3. 核心计算逻辑 =================
if st.button("🚀 启动复合交叉分析", use_container_width=True):
    # 1. 计算比分机构概率 (去水)
    scores_dict = {
        "1:0": 1/s_10, "2:0": 1/s_20, "2:1": 1/s_21, "3:0": 1/s_30, "3:1": 1/s_31,
        "3:2": 1/s_32, "4:0": 1/s_40, "4:1": 1/s_41, "4:2": 1/s_42, "5:0": 1/s_50,
        "5:1": 1/s_51, "5:2": 1/s_52, "胜其他": 1/s_swin_other,
        "0:0": 1/s_00, "1:1": 1/s_11, "2:2": 1/s_22, "3:3": 1/s_33, "平其他": 1/s_draw_other,
        "0:1": 1/s_01, "0:2": 1/s_02, "1:2": 1/s_12, "0:3": 1/s_03, "1:3": 1/s_13,
        "2:3": 1/s_23, "0:4": 1/s_04, "1:4": 1/s_14, "2:4": 1/s_24, "0:5": 1/s_05,
        "1:5": 1/s_15, "2:5": 1/s_25, "负其他": 1/s_lose_other
    }
    total_score_prob = sum(scores_dict.values())
    real_scores = {k: round((v / total_score_prob) * 100, 2) for k, v in scores_dict.items()}
    sorted_odds = sorted(real_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # 2. 纯数学泊松概率
    poisson_scores = {}
    score_mapping = {
        "0:0": (0,0), "1:0": (1,0), "2:0": (2,0), "3:0": (3,0), "4:0": (4,0), "5:0": (5,0),
        "0:1": (0,1), "1:1": (1,1), "2:1": (2,1), "3:1": (3,1), "4:1": (4,1), "5:1": (5,1),
        "0:2": (0,2), "1:2": (1,2), "2:2": (2,2), "3:2": (3,2), "4:2": (4,2), "5:2": (5,2),
        "0:3": (0,3), "1:3": (1,3), "2:3": (2,3), "3:3": (3,3), "0:4": (0,4), "1:4": (1,4), 
        "2:4": (2,4), "0:5": (0,5), "1:5": (1,5), "2:5": (2,5)
    }
    for score_str, (h, a) in score_mapping.items():
        prob_h = get_poisson(h, home_exp)
        prob_a = get_poisson(a, away_exp)
        poisson_scores[score_str] = round(prob_h * prob_a * 100, 2)
    sorted_poisson = sorted(poisson_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # 3. 校验总进球数概率 (去水)
    goals_dict = {"0球": 1/j_0, "1球": 1/j_1, "2球": 1/j_2, "3球": 1/j_3, "4球": 1/j_4, "5球": 1/j_5, "6球": 1/j_6, "7+球": 1/j_7}
    total_goals_prob = sum(goals_dict.values())
    real_goals = {k: round((v / total_goals_prob) * 100, 2) for k, v in goals_dict.items()}
    sorted_goals = sorted(real_goals.items(), key=lambda x: x[1], reverse=True)[:2]

    # ================= 4. 界面输出 =================
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.info("🏦 机构比分推算 Top 3")
        for i, (sc, pr) in enumerate(sorted_odds):
            st.write(f"**No.{i+1}** —— `{sc}` (`{pr}%`)")
            
    with col_m2:
        st.success("🔢 纯数学泊松比分 Top 3")
        for i, (sc, pr) in enumerate(sorted_poisson):
            st.write(f"**No.{i+1}** —— `{sc}` (`{pr}%`)")
            
    with col_m3:
        st.warning("⚽ 机构防范总进球 Top 2")
        for i, (gl, pr) in enumerate(sorted_goals):
            st.write(f"**{gl}** (`{pr}%`)")
            
    st.divider()
    
    # 偏离度对比
    top1_odds_score = sorted_odds[0][0]
    odds_prob = sorted_odds[0][1]
    pois_prob = poisson_scores.get(top1_odds_score, 0.0)
    diff = odds_prob - pois_prob
    
    st.subheader("🚨 意图与实力偏离度预警")
    st.write(f"机构最防范的比分是 `{top1_odds_score}`。")
    st.write(f"机构算出的去水概率为 `{odds_prob}%`，数学泊松算出的概率为 `{pois_prob}%`。")
    
    if diff > 3.0:
        st.error(f"⚠️ 警报：机构对比分 `{top1_odds_score}` 的防范力度远超纸面数学概率！可能存在【机构未公开的利好】！")
    elif diff < -3.0:
        st.warning(f"⚠️ 异常提示：纸面数学非常支持比分 `{top1_odds_score}`，但机构赔率显得无动于衷，小心大热倒灶。")
    else:
        st.info("👌 赔率概率与泊松概率基本吻合，属于正常实力盘。")
