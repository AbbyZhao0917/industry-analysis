"""
研究工具箱 —— 议题树生成 + 数据源推荐 + AI研究向导
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context

st.set_page_config(page_title="研究工具箱", page_icon="🧰", layout="wide")

st.title("🧰 研究工具箱")
st.caption("议题树生成 · 数据源推荐 · AI辅助研究流程")

research_question = st.text_area(
    "输入研究问题",
    placeholder="例如：如何评估连锁餐饮品牌的扩张潜力？",
    height=80,
)

col1, col2 = st.columns([1, 1])
with col1:
    do_tree = st.checkbox("生成议题树（MECE拆解）", value=True)
    do_sources = st.checkbox("推荐数据源", value=True)
with col2:
    do_ai = st.checkbox("AI工具建议", value=True)
    do_steps = st.checkbox("规划研究步骤", value=True)

start_btn = st.button("🧰 开始规划", type="primary", use_container_width=True)

if start_btn and research_question:
    kb_names = ["research-cookbook", "data-sources", "ai-research-guide"]
    system_prompt = build_system_context(kb_names)
    system_prompt += f"""

## 任务

针对研究问题「{research_question}」提供研究方案。

请根据以下勾选的模块输出：
- 议题树拆解(MECE)：{"是" if do_tree else "否"}
- 资讯来源推荐：{"是" if do_sources else "否"}（给出具体来源名称和网址）
- AI工具建议：{"是" if do_ai else "否"}
- 研究步骤规划（资讯料理法三阶段）：{"是" if do_steps else "否"}

### 数据源推荐要求
给出具体的来源名称和网址URL，不要只写类别。例如：
- 国家统计局社零数据：https://www.stats.gov.cn/...
- CCFA便利店报告：https://www.ccfa.org.cn/...
"""

    with st.spinner("规划中..."):
        try:
            response = ask_claude(system_prompt, f"请为「{research_question}」提供研究方案")
            st.success("✅ 研究方案已生成")
            st.markdown(response)
        except Exception as e:
            st.error(f"出错: {e}")

elif start_btn and not research_question:
    st.warning("请输入研究问题")

if not start_btn:
    st.info("👆 输入研究问题，点击「开始规划」")
    st.markdown("""
    ### 工具箱功能
    - **议题树生成**：MECE原则拆解研究问题
    - **数据源推荐**：匹配书中资源（统计机构/研报/数据库/专家网络/另类数据）
    - **AI工具建议**：适配研究阶段的AI工具推荐
    - **研究步骤**：资讯料理法三阶段（备菜→烹饪→摆盘）
    """)