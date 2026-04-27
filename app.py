
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import poisson

# --- 核心算法：泊松分布计算 ---
def calculate_matrix(home_expect, away_expect):
    max_g = 6
    h_probs = [poisson.pmf(i, home_expect) for i in range(max_g)]
    a_probs = [poisson.pmf(j, away_expect) for j in range(max_g)]
    return np.outer(h_probs, a_probs)

# --- 实战决策引擎 ---
class MatchAnalyzer:
    def __init__(self, data):
        self.data = data

    def run_strategy_check(self):
        warnings = []
        # 1. 对称赔率检查 (0球=5球, 10.0-13.0)
        if 10.0 <= self.data['zero_o'] <= 13.0 and abs(self.data['zero_o'] - self.data['five_o']) < 0.5:
            warnings.append("🚨 【策略1：对称赔率】触发！0球与5球赔率镜像平衡，谨防机构风险对冲。")
        
        # 2. 60倍标志位检查
        if 55.0 <= self.data['odd_34'] <= 65.0:
            warnings.append("⚠️ 【策略2：60倍标志位】3:4/4:3 处于敏感区间，注意高倍离群结果。")

        # 3. 38/30 屠杀模型
        if abs(self.data['zero_o'] - 38.0) < 1.0:
            warnings.append("🧨 【策略3：38/30屠杀模型】0球超高赔，历史指向大球屠杀赛果。")
            
        return warnings

# --- Streamlit 界面 ---
def main():
    st.set_page_config(page_title="AI数据分析站", layout="wide")
    st.title("📊 竞彩大数据实战工作站 V7.0")
    st.caption("基于 GitHub 版本管理 | 5:1 & 5:2 独立建模版")

    # --- 第一行：赛前基本面录入 ---
    st.header("1. 赛前数据录入 (基本面 + 指纹)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        h_name = st.text_input("主队名称", "阿森纳")
        a_name = st.text_input("客队名称", "曼城")
        league_rank = st.text_input("联赛排名对比", "2 vs 1")
    
    with col2:
        h_att = st.number_input("主队进攻系数 (场均进球)", value=1.8, step=0.1)
        a_def = st.number_input("客队防守系数 (场均失球)", value=1.0, step=0.1)
        h_def = st.number_input("主队防守系数", value=0.9, step=0.1)
        a_att = st.number_input("客队进攻系数", value=1.7, step=0.1)

    with col3:
        win = st.number_input("胜赔 (W)", value=2.15)
        draw = st.number_input("平赔 (D)", value=3.20)
        lose = st.number_input("负赔 (L)", value=3.40)
        st.divider()
        zero_o = st.number_input("0球赔率", value=12.0)
        five_o = st.number_input("5球赔率", value=12.0)
        odd_34 = st.number_input("3:4/4:3 标志位", value=60.0)

    # --- 第二行：执行分析 ---
    if st.button("🔥 立即执行三层逻辑比对分析"):
        # 计算预期进球
        h_exp = h_att * a_def
        a_exp = a_att * h_def
        
        # 运行引擎
        params = {
            'win': win, 'draw': draw, 'lose': lose,
            'zero_o': zero_o, 'five_o': five_o, 'odd_34': odd_34
        }
        analyzer = MatchAnalyzer(params)
        strategies = analyzer.run_strategy_check()
        
        # 获取概率矩阵
        matrix = calculate_matrix(h_exp, a_exp)

        # --- 展示分析结论 ---
        st.divider()
        res_l, res_r = st.columns([1, 2])
        
        with res_l:
            st.subheader("🚩 策略风险提示")
            for s in strategies:
                st.error(s)
            if not strategies:
                st.success("✅ 未发现明显反杀信号，盘面逻辑正常。")
            
            st.info(f"💡 建模预期：{h_name} ({h_exp:.2f}) : {a_name} ({a_exp:.2f})")

        with res_r:
            st.subheader("🎯 核心比分指纹匹配")
            
            scores = []
            # 常规比分循环
            for i in range(5):
                for j in range(5):
                    scores.append({"比分": f"{i}:{j}", "AI概率": f"{matrix[i,j]*100:.2f}%", "建议": "常规对标"})
            
            # 独立显示 5:1 和 5:2 (严格遵守你的要求)
            scores.append({"比分": "5:1", "AI概率": f"{matrix[5,1]*100:.2f}%", "建议": "独立高倍"})
            scores.append({"比分": "5:2", "AI概率": f"{matrix[5,2]*100:.2f}%", "建议": "独立高倍"})
            scores.append({"比分": "3:4", "AI概率": "重点监测", "建议": "标志位防御"})

            # 转为 DataFrame 并排序显示前 10 高频比分
            df = pd.DataFrame(scores)
            st.table(df.sort_values(by="AI概率", ascending=False).head(12))

if __name__ == "__main__":
    main()


