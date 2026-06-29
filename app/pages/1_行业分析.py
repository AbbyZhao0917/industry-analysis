"""
行业分析工作台 —— 基于七维度框架的行业分析
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context

st.set_page_config(page_title="行业分析", page_icon="📊", layout="wide")

st.title("📊 行业分析工作台")
st.caption("基于肖璟《如何快速了解一个行业》七维度框架 · 数据来源标注URL")

# ---- 输入区 ----
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    industry_name = st.text_input(
        "输入行业名称",
        placeholder="例如：预制菜、便利店、CPO、新能源车、银发经济...",
    )
with col2:
    analysis_depth = st.selectbox("分析深度", ["标准（3000-5000字）", "精简（1500字）", "深度（8000字+）"])
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    start_btn = st.button("🔍 开始分析", type="primary", use_container_width=True)

# ---- 分析过程 ----
if start_btn and industry_name:
    # 构建系统提示词（加载知识库）
    kb_names = [
        "industry-lifecycle",
        "business-model-canvas",
        "market-sizing",
        "moat-framework",
        "competitive-analysis",
        "valuation-guide",
        "pest-framework",
        "prosperity-tracking",
        "research-cookbook",
        "data-sources",
    ]
    system_prompt = build_system_context(kb_names)
    system_prompt += f"""

## 分析任务

对「{industry_name}」行业进行完整的七维度分析。

### 要求
1. 先搜索最新数据（市场规模、渗透率、政策、头部公司财报），每条数据标注具体来源URL和时间
2. 判断产业生命周期阶段（渗透率法 + 辅助信号）
3. 七维度逐一分析，根据生命周期阶段调整权重
4. 使用 SCQR 格式输出（情境→冲突→问题→方案）
5. 中文输出，分析深度：{analysis_depth}

### 数据来源强制要求
- 每条数据必须包含具体网址（URL），不得只写"XXX报告"或"XXX研究院"
- 格式示例：「2025年市场规模5033亿元（来源：https://www.huaon.com/channel/trend/1158078.html，华经产业研究院，2025）」
- 优先使用书中推荐的资源：国家统计局、行业协会官网、券商研报、专业数据库、公司招股书/年报
"""

    with st.spinner(f"正在分析「{industry_name}」行业..."):
        with st.expander("📡 实时搜索与数据处理中...", expanded=True):
            status_placeholder = st.empty()

        # 调用 Claude
        try:
            response = ask_claude(system_prompt, f"请分析「{industry_name}」行业")
            st.success(f"✅ 「{industry_name}」行业分析完成")
            st.markdown(response)
        except Exception as e:
            st.error(f"分析出错: {e}")

elif start_btn and not industry_name:
    st.warning("请输入行业名称")

# ---- 空状态提示 ----
if not start_btn:
    st.info("👆 输入行业名称，点击「开始分析」按钮")
    st.markdown("""
    ### 分析内容预览

    每次分析将覆盖以下七个维度：
    1. **可行性** — 商业模式画布 + 对标法验证 + UE模型
    2. **规模性** — TAM/SAM/SOM + 市场规模测算
    3. **防守性** — 护城河9子项评分卡
    4. **盈利性** — CRn集中度 + 五力模型 + 产业链利润分配
    5. **估值** — 生命周期对应估值方法
    6. **外部因素** — PEST四维分析 + 技术创新金字塔
    7. **景气度** — 关键指标识别 + 当前景气度判断

    *所有数据标注来源URL和时间 · 基于公开信息 · 不构成投资建议*
    """)