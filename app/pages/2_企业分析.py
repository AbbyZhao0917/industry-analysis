"""
企业分析工作台 —— 商业模式画布 + UE模型 + 护城河评分
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context

st.set_page_config(page_title="企业分析", page_icon="🏢", layout="wide")

st.title("🏢 企业分析工作台")
st.caption("商业模式画布 · UE单位经济模型 · 护城河评分卡 · 估值框架")

company_name = st.text_input("输入企业名称", placeholder="例如：明康汇、盒马、见福便利店...")
depth = st.selectbox("分析深度", ["标准", "精简", "深度"])
start_btn = st.button("🔍 开始分析", type="primary")

if start_btn and company_name:
    kb_names = [
        "business-model-canvas",
        "moat-framework",
        "competitive-analysis",
        "valuation-guide",
        "market-sizing",
    ]
    system_prompt = build_system_context(kb_names)
    system_prompt += f"""

## 分析任务

对「{company_name}」进行深度企业分析。分析深度：{depth}。

### 要求
1. 先搜索企业最新数据（财报/业务/竞争），每条数据标注具体来源URL和时间
2. 绘制商业模式画布（9要素完整填写）
3. 构建UE单位经济模型（填入具体数字或推估值并标注）
4. 护城河评分卡（9子项逐一评分1-5，每项给出理由）
5. 竞争定位 + 估值框架
6. 中文输出

### 数据来源强制要求
- 每条数据必须包含具体网址（URL）
- 格式：「营收382亿（来源：https://stock.finance.sina.com.cn/...，2025年报）」
"""

    with st.spinner(f"正在分析「{company_name}」..."):
        try:
            response = ask_claude(system_prompt, f"请分析「{company_name}」企业")
            st.success(f"✅ 「{company_name}」分析完成")
            st.markdown(response)
        except Exception as e:
            st.error(f"分析出错: {e}")

elif start_btn and not company_name:
    st.warning("请输入企业名称")

if not start_btn:
    st.info("👆 输入企业名称，点击「开始分析」")
    st.markdown("""
    ### 分析内容
    1. 企业概览 + 行业定位
    2. 商业模式画布（9要素表）
    3. UE单位经济模型（数值表格）
    4. 护城河评分卡（9项1-5分 + 总分/45）
    5. 竞争地位 + 估值框架
    6. 综合评估 + 风险提示
    """)