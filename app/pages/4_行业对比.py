"""
行业对比工作台 —— 两个行业七维度并排对比
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context

st.set_page_config(page_title="行业对比", page_icon="📈", layout="wide")

st.title("📈 行业对比工作台")
st.caption("两个行业七维度并排对比 · 差异高亮 · 选择建议")

col_a, col_b = st.columns(2)
with col_a:
    industry_a = st.text_input("行业 A", placeholder="例如：生鲜电商")
with col_b:
    industry_b = st.text_input("行业 B", placeholder="例如：社区团购")

start_btn = st.button("📈 开始对比", type="primary", use_container_width=True)

if start_btn and industry_a and industry_b:
    kb_names = [
        "industry-lifecycle",
        "business-model-canvas",
        "market-sizing",
        "moat-framework",
        "competitive-analysis",
        "valuation-guide",
        "pest-framework",
        "prosperity-tracking",
    ]
    system_prompt = build_system_context(kb_names)
    system_prompt += f"""

## 分析任务

对「{industry_a}」和「{industry_b}」两个行业进行七维度并排对比。

### 要求
1. 分别定位两个行业的生命周期阶段
2. 七维度逐一并排对比：可行性/规模性/防守性/盈利性/估值/外部因素/景气度
3. 每个维度呈现两个行业的最新数据（标注来源URL和时间）
4. 差异高亮 + 选择矩阵（成长性/确定性/长期价值角度）
5. 综合建议 + 风险提示

### 数据来源强制要求
每条数据必须标注具体来源URL和时间
"""

    with st.spinner(f"正在对比「{industry_a}」vs「{industry_b}」..."):
        try:
            response = ask_claude(system_prompt, f"请对比分析「{industry_a}」和「{industry_b}」两个行业")
            st.success(f"✅ 对比完成")
            st.markdown(response)
        except Exception as e:
            st.error(f"分析出错: {e}")

elif start_btn and not (industry_a and industry_b):
    st.warning("请输入两个行业名称")

if not start_btn:
    st.info("👆 输入两个行业名称，点击「开始对比」")