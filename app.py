import streamlit as st
import numpy as np
import math

st.set_page_config(page_title="Soccer Odds V4", layout="wide")

st.title("🔥 竞彩全赔率 + 泊松模型复合分析器")
st.write("结合机构去水概率与纯数学泊松分布，深度挖掘比分底牌。")
st.divider()

# ================= 1. 泊松分布纯算法（无需第三方包） =================
def get_poisson(k, lamb):
    """手动计算泊松分布，防止服务器缺少scipy包"""
    if lamb <= 0:
        return 0.0
    return (math.pow(lamb, k) * math.exp(-lamb)) / math.factorial(k)

st.sidebar.header("📊 泊松模型：预期进球设定")
home_exp = st.sidebar.slider("主队预期进球数", 0.1, 5.0, 1.5, 0.05)
away_exp = st.sidebar.slider("客队预期进球数", 0.1, 5.0, 1.2, 0.05)

# ================= 2. 基础赔率录入 =================
with st.expander("📊 1. 基础胜平负赔率录入", expanded=True):
    col1, col2, col3 = st.columns(3)
    spf_s = col1.number_input("胜 (Home Win)", 1.0, 1000.0, 3.92, 0.01)
    spf_p = col2.number_input("平 (Draw)", 1.0, 1000.0, 3.30, 0.01)
    spf_f = col3.number_input("负 (Away Win)", 1.0, 1000.0, 1.75, 0.01)

with st.expander("🏁 2. 竞彩比分赔率录入", expanded=True):
    st.write("【主胜比分】")
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    s_10 = sc1.number_input("1:0", 1.0, 1000.0, 11.0, 0.1)
    s_20 = sc2.number_input("2:0", 1.0, 1000.0, 22.0, 0.1)
    s_21 = sc3.number_input("2:1", 1.0, 1000.0, 12.0, 0.1)
    s_30 = sc4.number_input("3:0", 1.0, 1000.0, 55.0, 0.1)
    s_31 = sc5.number_input("3:1", 1.0, 1000.0, 32.0, 0.1)
    
    st.write("【平局比分】")
    sc15, sc16, sc17 = st.columns(3)
    s_00 = sc15.number_input("0:0", 1.0, 1000.0, 12.0, 0.1)
    s_11 = sc16.number_input("1:1", 1.0, 1000.0, 6.3, 0.1)
    s_22 = sc17.number_input("2:2", 1.0, 1000.0, 14.0, 0.1)
    
    st.write("【客胜比分】")
    sc20, sc21, sc22, sc23 = st.columns(4)
    s_01 = sc20.number_input("0:1", 1.0, 1000.0, 7.0, 0.1)
    s_02 = sc21.number_input("0:2", 1.0, 1000.0, 8.0, 0.1)
    s_12 = sc22.number_input("1:2", 1.0, 1000.0, 7.0, 0.1)
    s_03 = sc23.number_input("0:3", 1.0, 1000.0, 15.0, 0.1)

st.divider()

# ================= 3. 核心计算逻辑 =================
if st.button("🚀 启动复合交叉分析", use_container_width=True):
    # 计算比分机构概率 (去水)
    scores_dict = {
        "1:0": 1/s_10, "2:0": 1/s_20, "2:1": 1/s_21, "3:0": 1/s_30, "3:1": 1/s_31,
        "0:0": 1/s_00, "1:1": 1/s_11, "2:2": 1/s_22,
        "0:1": 1/s_01, "0:2": 1/s_02, "1:2": 1/s_12, "0:3": 1/s_03
    }
    total_score_prob = sum(scores_dict.values())
    real_scores = {k: round((v / total_score_prob) * 100, 2) for k, v in scores_dict.items()}
    
    # 获取赔率Top 3
    sorted_odds = sorted(real_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # 纯数学泊松概率
    poisson_scores = {}
    score_mapping = {
        "0:0": (0,0), "1:0": (1,0), "2:0": (2,0), "3:0": (3,0),
        "0:1": (0,1), "1:1": (1,1), "2:1": (2,1), "3:1": (3,1),
        "0:2": (0,2), "1:2": (1,2), "2:2": (2,2), "0:3": (0,3)
    }
    for score_str, (h, a) in score_mapping.items():
        prob_h = get_poisson(h, home_exp)
        prob_a = get_poisson(a, away_exp)
        poisson_scores[score_str] = round(prob_h * prob_a * 100, 2)
        
    sorted_poisson = sorted(poisson_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # ================= 4. 界面输出 =================
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.info("🏦 机构赔率推算 Top 3")
        for i, (sc, pr) in enumerate(sorted_odds):
            st.write(f"**No.{i+1}** —— 比分 `{sc}` (概率 `{pr}%`)")
            
    with col_m2:
        st.success("🔢 纯数学泊松模型 Top 3")
        for i, (sc, pr) in enumerate(sorted_poisson):
            st.write(f"**No.{i+1}** —— 比分 `{sc}` (概率 `{pr}%`)")
            
    st.divider()
    
    # 偏离度对比
    top1_odds_score = sorted_odds[0][0]
    odds_prob = sorted_odds[0][1]
    pois_prob = poisson_scores.get(top1_odds_score, 0.0)
    diff = odds_prob - pois_prob
    
    st.subheader("🚨 意图与实力偏离度预警")
    st.write(f"机构最防范的比分是 `{top1_odds_score}`。")
    st.write(f"机构算出的概率为 `{odds_prob}%`，数学泊松算出的概率为 `{pois_prob}%`。")
    
    if diff > 3.0:
        st.error(f"⚠️ 警报：机构对比分 `{top1_odds_score}` 的防范力度远超纸面数学概率！可能存在【机构未公开的利好】！")
    elif diff < -3.0:
        st.warning(f"⚠️ 异常提示：纸面数学非常支持比分 `{top1_odds_score}`，但机构赔率显得无动于衷，小心大热倒灶。")
    else:
        st.info("👌 赔率概率与泊松概率基本吻合，属于正常实力盘。")
