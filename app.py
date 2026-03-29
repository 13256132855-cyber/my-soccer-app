
import streamlit as st
import numpy as np
import scipy.stats as stats

st.set_page_config(page_title="Jingcai Full Odds Analyzer v4.0", layout="wide")

st.title("🔥 竞彩全赔率 + 泊松分布复合分析器 v4.0")
st.write("结合机构赔率去水概率与数学泊松分布，深度挖掘比分底牌。")
st.divider()

# ================= 侧边栏：泊松分布预期输入 =================
st.sidebar.header("📊 泊松模型：预期进球设定")
st.sidebar.write("根据两队近期攻防，输入你预期的进球率：")
home_exp = st.sidebar.slider("主队预期进球数", 0.1, 5.0, 1.5, 0.05)
away_exp = st.sidebar.slider("客队预期进球数", 0.1, 5.0, 1.2, 0.05)

# 计算泊松分布比分矩阵 (0-5球)
poisson_matrix = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        prob_i = stats.poisson.pmf(i, home_exp)
        prob_j = stats.poisson.pmf(j, away_exp)
        poisson_matrix[i, j] = prob_i * prob_j

# ================= 主界面：赔率录入 =================
# 1. 胜平负
with st.expander("📊 1. 基础胜平负赔率录入", expanded=True):
    col1, col2, col3 = st.columns(3)
    spf_s = col1.number_input("胜 (Home Win)", 1.0, 1000.0, 3.92, 0.01)
    spf_p = col2.number_input("平 (Draw)", 1.0, 1000.0, 3.30, 0.01)
    spf_f = col3.number_input("负 (Away Win)", 1.0, 1000.0, 1.75, 0.01)

# 2. 比分 (31项)
with st.expander("🏁 2. 竞彩比分赔率录入", expanded=True):
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

if st.button("🚀 启动复合交叉分析", use_container_width=True):
    # 1. 基础概率计算
    sum_prob = (1/spf_s) + (1/spf_p) + (1/spf_f)
    payout = round((1 / sum_prob) * 100, 2)
    
    # 2. 31个比分去水计算
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
    
    # 转换为真实去水概率
    real_scores = {k: round((v / total_score_prob) * 100, 2) for k, v in scores_dict.items()}
    
    # ================= 模块一：比分区间聚类 =================
    st.subheader("📊 模块一：三路大军比分聚类 (Cluster Analysis)")
    
    home_cluster = sum([real_scores[k] for k in ["1:0", "2:0", "2:1", "3:0", "3:1", "3:2", "4:0", "4:1", "4:2", "5:0", "5:1", "5:2", "胜其他"]])
    draw_cluster = sum([real_scores[k] for k in ["0:0", "1:1", "2:2", "3:3", "平其他"]])
    away_cluster = sum([real_scores[k] for k in ["0:1", "0:2", "1:2", "0:3", "1:3", "2:3", "0:4", "1:4", "2:4", "0:5", "1:5", "2:5", "负其他"]])
    
    col_h, col_d, col_a = st.columns(3)
    col_h.metric("主胜所有比分总概率", f"{round(home_cluster, 2)}%")
    col_d.metric("平局所有比分总概率", f"{round(draw_cluster, 2)}%")
    col_a.metric("客胜所有比分总概率", f"{round(away_cluster, 2)}%")
    
    # ================= 模块二：双模型Top比分对碰 =================
    st.subheader("🎯 模块二：双模型最可能比分 PK")
    
    # 赔率模型Top 3
    sorted_odds = sorted(real_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # 泊松模型Top 3
    poisson_scores = {}
    score_mapping = {
        "0:0": (0,0), "1:0": (1,0), "2:0": (2,0), "3:0": (3,0), "4:0": (4,0), "5:0": (5,0),
        "0:1": (0,1), "1:1": (1,1), "2:1": (2,1), "3:1": (3,1), "4:1": (4,1), "5:1": (5,1),
        "0:2": (0,2), "1:2": (1,2), "2:2": (2,2), "3:2": (3,2), "4:2": (4,2), "5:2": (5,2),
        "0:3": (0,3), "1:3": (1,3), "2:3": (2,3), "3:3": (3,3),
        "0:4": (0,4), "1:4": (1,4), "2:4": (2,4),
        "0:5": (0,5), "1:5": (1,5), "2:5": (2,5)
    }
    
    for score_str, (h, a) in score_mapping.items():
        poisson_scores[score_str] = round(poisson_matrix[h, a] * 100, 2)
        
    sorted_poisson = sorted(poisson_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.info("🏦 机构赔率推算 Top 3 (金钱意志)")
        for i, (sc, pr) in enumerate(sorted_odds):
            st.write(f"**No.{i+1}** —— 比分 `{sc}` (概率 `{pr}%`)")
            
    with col_m2:
        st.success("🔢 泊松数学模型 Top 3 (纸面实力)")
        for i, (sc, pr) in enumerate(sorted_poisson):
            st.write(f"**No.{i+1}** —— 比分 `{sc}` (概率 `{pr}%`)")
            
    st.divider()
    
    # ================= 模块三：偏离度预警 =================
    st.subheader("🚨 模块三：机构意图与纸面实力偏离度预警")
    
    # 检查赔率最看好的比分在泊松里热不热
    top1_odds_score = sorted_odds[0][0]
    odds_prob = sorted_odds[0][1]
    
    if top1_odds_score in poisson_scores:
        pois_prob = poisson_scores[top1_odds_score]
        diff = odds_prob - pois_prob
        
        st.write(f"机构最防范的比分是 `{top1_odds_score}`。")
        st.write(f"机构给出的真实概率为 `{odds_prob}%`，而根据两队进球率算出的纯数学概率为 `{pois_prob}%`。")
        
        if diff > 5.0:
            st.error(f"⚠️ 强烈警报：机构对比分 `{top1_odds_score}` 的防范力度远超纸面数学概率（偏高 {round(diff,2)}%）！极大概率存在【机构未公开的利好】或【严重诱导】！")
        elif diff < -5.0:
            st.warning(f"⚠️ 异常提示：纸面数学非常支持比分 `{top1_odds_score}`，但机构赔率却显得无动于衷（偏低 {round(abs(diff),2)}%），小心大热倒灶。")
        else:
            st.info("👌 赔率概率与泊松概率基本吻合，属于正常实力盘。")
    else:
        st.warning(f"机构最防范的比分 `{top1_odds_score}` 超出了基础泊松（5球以内）的计算范围，属于极端大比分。")
