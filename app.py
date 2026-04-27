
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# ==========================================
# 1. 核心算法：泊松分布 + 极端赛果修正
# ==========================================
def calculate_advanced_matrix(h_lambda, a_lambda):
    """生成比分矩阵，并确保 5:1, 5:2 独立计算"""
    max_goals = 7  # 提升维度以覆盖大比分
    h_probs = [poisson.pmf(i, h_lambda) for i in range(max_goals)]
    a_probs = [poisson.pmf(j, a_lambda) for j in range(max_goals)]
    return np.outer(h_probs, a_probs)

# ==========================================
# 2. 深度逻辑模块：冷门、大球、高赔监控
# ==========================================
class EliteAnalyzer:
    def __init__(self, odds_data):
        self.odds = odds_data

    def monitor_anomalies(self):
        """自动捕捉冷门与大球信号"""
        signals = []
        
        # A. 冷门模块：基于平赔与 0:2/1:2 镜像
        if 2.10 <= self.odds['w'] <= 2.40 and self.odds['d'] < 3.00:
            signals.append("📉 【冷门模块】命中：平赔压低且主胜不稳，谨防 0:1 / 0:2 冷门坐标。")
            
        # B. 大球模块：38/30 屠杀模型 + 对称赔率
        if abs(self.odds['zero_o'] - self.odds['five_o']) < 0.5 and 10 <= self.odds['zero_o'] <= 13:
            signals.append("💣 【大球模块】触发：0/5球对称防御，庄家预期进球数极可能发生离群大球。")
        elif self.odds['zero_o'] > 35:
            signals.append("🧨 【大球模块】触发：0球赔率过载，系统判定本场无平局可能，直指大比分。")

        # C. 高赔率坐标：60倍标志位
        if 55 <= self.odds['odd_34'] <= 65:
            signals.append("🎯 【高赔模块】捕捉：比分坐标 3:4/4:3 出现 60倍核心标志位，必防项。")
            
        return signals

# ==========================================
# 3. Streamlit 交互界面
# ==========================================
def main():
    st.set_page_config(page_title="AI 竞彩实战分析器", layout="wide")
    st.title("🏆 AI 竞彩大数据全能分析器")
    st.subheader("集成：冷门比分库 + 大球屠杀模型 + 高赔标志位")

    # --- 布局：左侧录入，右侧分析 ---
    with st.sidebar:
        st.header("📋 赛前数据录入")
        h_team = st.text_input("主队", "主队")
        a_team = st.text_input("客队", "客队")
        
        st.divider()
        st.write("⚽ 基本面系数")
        col_la, col_lb = st.columns(2)
        with col_la:
            h_att = st.number_input("主进攻", value=1.5)
            h_def = st.number_input("主防守", value=1.0)
        with col_lb:
            a_att = st.number_input("客进攻", value=1.2)
            a_def = st.number_input("客防守", value=1.1)
            
        st.divider()
        st.write("📊 赔率指纹")
        w = st.number_input("胜赔 (W)", value=2.25)
        d = st.number_input("平赔 (D)", value=3.10)
        l = st.number_input("负赔 (L)", value=3.40)
        
        st.write("🧭 避杀标志位")
        z_o = st.number_input("0球赔率", value=12.0)
        f_o = st.number_input("5球赔率", value=12.0)
        o_34 = st.number_input("3:4/4:3 赔率", value=60.0)

    # --- 分析执行 ---
    if st.button("🚀 启动深度建模分析"):
        # 计算 Lambda
        h_exp = h_att * a_def
        a_exp = a_att * h_def
        
        # 引擎扫描
        analyzer = EliteAnalyzer({'w':w, 'd':d, 'l':l, 'zero_o':z_o, 'five_o':f_o, 'odd_34':o_34})
        alerts = analyzer.monitor_anomalies()
        matrix = calculate_advanced_matrix(h_exp, a_exp)

        # --- 结果展示 ---
        st.divider()
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.error("🚨 异常预警")
            for alert in alerts:
                st.write(alert)
            if not alerts:
                st.success("常规盘面，未检测到离群信号")
            
            st.info(f"💡 泊松预测 Lambda: {h_exp:.2f} : {a_exp:.2f}")

        with c2:
            st.warning("🎯 建议比分 (已独立 5:1/5:2)")
            
            res = []
            # 获取常规高概率比分
            for i in range(5):
                for j in range(5):
                    res.append({"比分": f"{i}:{j}", "概率": f"{matrix[i,j]*100:.2f}%", "类型": "常规项"})
            
            # 强制插入你的“必防”坐标
            res.append({"比分": "5:1", "概率": f"{matrix[5,1]*100:.2f}%", "类型": "独立高倍"})
            res.append({"比分": "5:2", "概率": f"{matrix[5,2]*100:.2f}%", "类型": "独立高倍"})
            res.append({"比分": "3:4", "概率": "标志位", "类型": "冷门防御"})
            res.append({"比分": "胜其他", "概率": "计算中", "类型": "极端赛果"})

            df = pd.DataFrame(res).sort_values(by="概率", ascending=False)
            st.table(df.head(12))

if __name__ == "__main__":
    main()


