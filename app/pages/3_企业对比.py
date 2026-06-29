"""
企业对比工作台 —— 两家企业并排PK
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context

st.set_page_config(page_title="企业对比", page_icon="⚔️", layout="wide")

st.title("⚔️ 企业对比工作台")
st.caption("商业模式画布 · UE模型 · 护城河评分 · 估值 逐项PK")

col_a, col_b = st.columns(2)
with col_a:
    company_a = st.text_input("企业 A", placeholder="例如：盒马")
with col_b:
    company_b = st.text_input("企业 B", placeholder="例如：叮咚买菜")

start_btn = st.button("⚔️ 开始对比", type="primary", use_container_width=True)

if start_btn and company_a and company_b:
    kb_names = [
        "business-model-canvas",
        "moat-framework",
        "competitive-analysis",
        "valuation-guide",
    ]
    system_prompt = build_system_context(kb_names)
    system_prompt += f"""

## 分析任务

对「{company_a}」和「{company_b}」进行并排对比分析。

### 对比维度
1. 商业模式画布PK（9要素并排表）
2. UE模型关键指标PK（客单价、毛利率、净利率、回本周期等）
3. 护城河评分PK（9子项逐项评分 + 总分）
4. 竞争定位对比
5. 估值对比

### 最终输出
- 维度胜负统计（各赢几个维度）
- 各自优势场景
- 核心差异总结
- 选择建议

### 数据来源强制要求
每条数据必须标注具体来源URL和时间
"""

    with st.spinner(f"正在对比「{company_a}」vs「{company_b}」..."):
        try:
            response = ask_claude(system_prompt, f"请对比分析「{company_a}」和「{company_b}」两家企业")
            st.success(f"✅ 对比完成")
            st.markdown(response)
        except Exception as e:
            st.error(f"分析出错: {e}")

elif start_btn and not (company_a and company_b):
    st.warning("请输入两家企业名称")

if not start_btn:
    st.info("👆 输入两家企业名称，点击「开始对比」")
    st.markdown("""
    ### 对比维度
    | 维度 | 内容 |
    |------|------|
    | 商业模式画布 | 9要素并排对比 |
    | UE模型指标 | 客单价/毛利率/净利率/回本周期 |
    | 护城河PK | 9项评分1-5分逐项对比 |
    | 竞争定位 | 市场份额/产业链议价力 |
    | 估值对比 | PE/PB/PS + 估值水位判断 |
    """)