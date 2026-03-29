
import streamlit as st
import numpy as np

st.set_page_config(page_title="足球概率模拟器", layout="centered")

st.title("⚽ 智胜 AI 足球模拟器")
st.write("输入两队进球率来模拟比赛结果。")
st.divider()

st.header("📊 输入比赛基础数据")
home_lambda = st.slider("主队预期进球率", 0.1, 5.0, 1.5, 0.1)
away_lambda = st.slider("客队预期进球率", 0.1, 5.0, 1.2, 0.1)
sim_count = st.selectbox("模拟比赛场次", [1000, 10000, 50000], index=1)

if st.button("🎮 开始模拟分析", use_container_width=True):
    home_goals = np.random.poisson(home_lambda, sim_count)
    away_goals = np.random.poisson(away_lambda, sim_count)
    
    home_wins = np.sum(home_goals > away_goals)
    draws = np.sum(home_goals == away_goals)
    away_wins = np.sum(home_goals < away_goals)
    
    hw_prob = round((home_wins / sim_count) * 100, 2)
    d_prob = round((draws / sim_count) * 100, 2)
    aw_prob = round((away_wins / sim_count) * 100, 2)
    
    st.success("🎉 模拟完成！")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🏠 主胜率", str(hw_prob) + "%")
    col2.metric("🤝 平局率", str(d_prob) + "%")
    col3.metric("🚌 客胜率", str(aw_prob) + "%")
    
    st.subheader("📋 常见比分概率预测")
    scores = {}
    for h in range(4):
        for a in range(4):
            match_count = np.sum((home_goals == h) & (away_goals == a))
            prob = round((match_count / sim_count) * 100, 2)
            scores[str(h) + ":" + str(a)] = str(prob) + "%"
            
    sorted_scores = sorted(scores.items(), key=lambda x: float(x[1].replace('%', '')), reverse=True)[:5]
    
    for score, p in sorted_scores:
        st.write("比分 **" + score + "** 的预计发生概率：**" + p + "**")
