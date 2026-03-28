
import streamlit as st
import numpy as np

st.set_page_config(page_title="足球概率模拟器", layout="centered")

st.title("⚽ 智胜 AI 足球模拟器")
st.write("通过蒙特卡洛算法，输入两队进球率来模拟比赛结果。")

# 侧边栏输入
st.sidebar.header("📊 输入比赛基础数据")
home_lambda = st.sidebar.slider("主队预期进球率 (Poisson)", 0.1, 5.0, 1.5, 0.1)
away_lambda = st.sidebar.slider("客队预期进球率 (Poisson)", 0.1, 5.0, 1.2, 0.1)
sim_count = st.sidebar.selectbox("模拟比赛场次", [1000, 10000, 50000], index=1)

if st.sidebar.button("🎮 开始模拟分析", use_container_width=True):
    # 蒙特卡洛模拟
    home_goals = np.random.poisson(home_lambda, sim_count)
    away_goals = np.random.poisson(away_lambda, sim_count)
    
    home_wins = np.sum(home_goals > away_goals)
    draws = np.sum(home_goals == away_goals)
    away_wins = np.sum(home_goals < away_goals)
    
    # 转换百分比
    hw_prob = (home_wins / sim_count) * 100
    d_prob = (draws / sim_count) * 100
    aw_prob = (away_wins / sim_count) * 100
    
    st.success("🎉 模拟完成！结果如下：")
    
    # 指标展示
    col1, col2, col3 = st.columns(3)
    col1.metric("🏠 主胜率", f"{hw_prob:.2f}%")
    col2.metric("🤝 平局率", f"{d_prob:.2f}%")
    col3.metric("🚌 客胜率", f"{aw_prob:.2f}%")
    
    # 详细表格
    st.subheader("📋 常见比分概率预测")
    scores = {}
    for h in range(4):
        for a in range(4):
            match_count = np.sum((home_goals == h) & (away_goals == a))
            prob = (match_count / sim_count) * 100
            scores[f"{h}:{a}"] = f"{prob:.2f}%"
            
    # 展示前5个高频比分
    sorted_scores = sorted(scores.items(), key=lambda x: float(x[1].replace('%', '')), reverse=True)[:5]
    
    for score, p in sorted_scores:
        st.write(f"比分 **{score}** 的预计发生概率：**{p}**")
