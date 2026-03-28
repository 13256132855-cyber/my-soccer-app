import streamlit as st
import numpy as np

# 1. 手机端页面大字号优化
st.set_page_config(page_title="AI足球决策", layout="centered")
st.title("🛡️ 智胜 AI 足球模拟器")
st.caption("蒙特卡洛引擎 | 手机端专属纯净版")

# 2. 模拟计算引擎
def run_simulation(h_xg, a_xg, n=10000):
    # 用泊松分布模拟10,000次比赛进球数
    h_goals = np.random.poisson(h_xg, n)
    a_goals = np.random.poisson(a_xg, n)
    
    # 统计胜平负概率
    h_win = (h_goals > a_goals).mean()
    draw = (h_goals == a_goals).mean()
    a_win = (h_goals < a_goals).mean()
    return h_win, draw, a_win

# 3. 手机端卡片式交互
with st.container():
    st.subheader("📊 输入两队预期进球 (xG)")
    
    # 手机端大滑块，极易操作
    h_xg = st.slider("🏠 主队进攻权重 (xG)", 0.5, 4.0, 1.5, step=0.1)
    a_xg = st.slider("🚌 客队进攻权重 (xG)", 0.5, 4.0, 1.2, step=0.1)
    
    st.divider()
    
    # 点击按钮开始模拟
    if st.button("🚀 开始 10,000 次模拟"):
        hw, d, aw = run_simulation(h_xg, a_xg)
        
        # 结果展示
        col1, col2, col3 = st.columns(3)
        col1.metric("🏠 主胜率", f"{hw:.1%}")
        col2.metric("🤝 平局率", f"{d:
