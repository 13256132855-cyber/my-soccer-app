
import streamlit as st
import numpy as np

st.set_page_config(page_title="竞彩全赔率分析器", layout="centered")

st.title("🎯 竞彩全赔率操盘分析器")
st.write("将一场比赛的各项赔率录入系统，交叉验证机构的真实意图。")
st.divider()

# 1. 胜平负/让球
with st.expander("📊 1. 胜平负 / 让球胜平负 赔率录入", expanded=True):
    col1, col2, col3 = st.columns(3)
    spf_s = col1.number_input("胜 (主胜)", 1.0, 100.0, 2.10, 0.01)
    spf_p = col2.number_input("平", 1.0, 100.0, 3.20, 0.01)
    spf_f = col3.number_input("负", 1.0, 100.0, 3.10, 0.01)
    
    st.write("让球盘口 (可选)")
    col4, col5, col6, col7 = st.columns(4)
    rq_line = col4.text_input("让球数", "-1")
    rq_s = col5.number_input("让胜", 1.0, 100.0, 4.10, 0.01)
    rq_p = col6.number_input("让平", 1.0, 100.0, 3.75, 0.01)
    rq_f = col7.number_input("让负", 1.0, 100.0, 1.60, 0.01)

# 2. 总进球数
with st.expander("⚽ 2. 总进球数赔率录入", expanded=False):
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    g0 = g_col1.number_input("0球", 1.0, 100.0, 9.50, 0.01)
    g1 = g_col2.number_input("1球", 1.0, 100.0, 4.30, 0.01)
    g2 = g_col3.number_input("2球", 1.0, 100.0, 3.30, 0.01)
    g3 = g_col4.number_input("3球", 1.0, 100.0, 3.75, 0.01)
    
    g_col5, g_col6, g_col7, g_col8 = st.columns(4)
    g4 = g_col5.number_input("4球", 1.0, 100.0, 5.40, 0.01)
    g5 = g_col6.number_input("5球", 1.0, 100.0, 9.50, 0.01)
    g6 = g_col7.number_input("6球", 1.0, 100.0, 16.0, 0.1)
    g7 = g_col8.number_input("7+球", 1.0, 100.0, 26.0, 0.1)

# 3. 半全场
with st.expander("⏳ 3. 半全场赔率录入 (精简高频)", expanded=False):
    b_col1, b_col2, b_col3 = st.columns(3)
    b_ss = b_col1.number_input("胜胜", 1.0, 100.0, 3.30, 0.01)
    b_ps = b_col2.number_input("平胜", 1.0, 100.0, 5.00, 0.01)
    b_pp = b_col3.number_input("平平", 1.0, 100.0, 4.80, 0.01)
    
    b_col4, b_col5, b_col6 = st.columns(3)
    b_pf = b_col4.number_input("平负", 1.0, 100.0, 6.75, 0.01)
    b_ff = b_col5.number_input("负负", 1.0, 100.0, 5.00, 0.01)
    b_others = b_col6.number_input("其他半全场均值", 1.0, 100.0, 15.0, 0.1)

# 4. 经典波胆比分
with st.expander("🏁 4. 核心比分赔率录入", expanded=False):
    s_col1, s_col2, s_col3 = st.columns(3)
    s_10 = s_col1.number_input("1:0", 1.0, 100.0, 6.50, 0.01)
    s_20 = s_col2.number_input("2:0", 1.0, 100.0, 9.50, 0.01)
    s_21 = s_col3.number_input("2:1", 1.0, 100.0, 8.00, 0.01)
    
    s_col4, s_col5, s_col6 = st.columns(3)
    s_00 = s_col4.number_input("0:0", 1.0, 100.0, 9.50, 0.01)
    s_11 = s_col5.number_input("1:1", 1.0, 100.0, 6.00, 0.01)
    s_22 = s_col6.number_input("2:2", 1.0, 100.0, 13.0, 0.1)
    
    s_col7, s_col8, s_col9 = st.columns(3)
    s_01 = s_col7.number_input("0:1", 1.0, 100.0, 8.50, 0.01)
    s_02 = s_col8.number_input("0:2", 1.0, 100.0, 15.0, 0.1)
    s_12 = s_col9.number_input("1:2", 1.0, 100.0, 10.0, 0.1)

st.divider()

# 计算与分析
if st.button("🔍 开启全赔率交叉验证", use_container_width=True):
    st.success("📊 核心数据解析完成！")
    
    # 1. 计算理论概率与机构返还率
    sum_prob = (1/spf_s) + (1/spf_p) + (1/spf_f)
    payout = round((1 / sum_prob) * 100, 2)
    
    real_s = round(((1/spf_s) / sum_prob) * 100, 2)
    real_p = round(((1/spf_p) / sum_prob) * 100, 2)
    real_f = round(((1/spf_f) / sum_prob) * 100, 2)
    
    st.subheader("💡 机构返还率与真实概率")
    st.write(f"该场比赛机构整体返还率约为：**{payout}%**")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("真实胜率", f"{real_s}%")
    c2.metric("真实平率", f"{real_p}%")
    c3.metric("真实负率", f"{real_f}%")
    
    st.divider()
    
    # 2. 简易异常坐标逻辑筛查
    st.subheader("🛡️ 操盘逻辑漏洞筛查")
    anomalies = 0
    
    # 漏洞1：0球赔率与比分0:0冲突
    if abs((1/g0) - (1/s_00)) > 0.05:
         st.warning("⚠️ 【异常提示】总进球数 0 球与比分 0:0 赔率存在数学剪刀差，机构可能在其中一项上进行了刻意诱导。")
         anomalies += 1
         
    # 漏洞2：平局概率与1:1比分冲突
    if real_p > 35.0 and s_11 > 6.5:
        st.warning("⚠️ 【异常提示】胜平负体系中平局概率较高，但比分1:1的赔率却偏高。机构可能在刻意阻绝高频平局比分的资金。")
        anomalies += 1
        
    # 漏洞3：总进球大球偏向
    prob_big = (1/g3) + (1/g4) + (1/g5)
    if prob_big > 0.5 and (s_10 < 6.0 or s_01 < 7.0):
        st.info("ℹ️ 【操盘提示】总进球倾向于大球（3球及以上），但 1:0 或 0:1 的小比分赔率却压得很低，存在诱小防大可能。")
        anomalies += 1
        
    if anomalies == 0:
        st.info("✅ 暂未在核心录入赔率中发现明显逻辑冲突，机构盘面较为平衡。")

    st.divider()
    st.subheader("📌 提示")
    st.caption("该系统目前为 V1.0 赔率接入版。如需更精准捕捉 abnormal coordinates（异常坐标）或执行 game theory（博弈）镜像对比，我们接下来需要建立更庞大的底层赔率库。")
