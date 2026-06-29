"""
研究工具箱 —— 议题树生成 · 数据源推荐 · AI 辅助研究流程
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import markdown
import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context
from app.utils.style import inject_css
from app.utils.search import search_web

st.set_page_config(page_title="研究工具箱 · 经纬", page_icon="◈", layout="wide")

inject_css()

st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">研究工具箱</h1>'
    '<div class="page-subtitle">议题树生成 &middot; 数据源推荐 &middot; AI 辅助研究流程</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 输入区 ----
st.markdown('<div class="card">', unsafe_allow_html=True)

research_question = st.text_area(
    "输入研究问题",
    placeholder="例如：如何评估连锁餐饮品牌的扩张潜力？",
    height=80,
    label_visibility="collapsed",
)

col1, col2 = st.columns([1, 1])
with col1:
    do_tree = st.checkbox("生成议题树（MECE 拆解）", value=True)
    do_sources = st.checkbox("推荐数据源", value=True)
with col2:
    do_ai = st.checkbox("AI 工具建议", value=True)
    do_steps = st.checkbox("规划研究步骤", value=True)

start_btn = st.button("开始规划", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---- 分析执行 ----
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

    # 联网搜索
    search_results = search_web(research_question)
    system_prompt += f"\n\n## 联网搜索结果（最新公开数据）\n\n{search_results}\n\n请基于以上搜索结果，结合方法论框架进行分析。"

    with st.spinner("正在生成研究方案..."):
        try:
            response = ask_claude(system_prompt, f"请为「{research_question}」提供研究方案")
            html_body = markdown.markdown(response, extensions=['tables', 'fenced_code'])

            st.markdown(f"""
            <div class="report-container">
                <div class="report-header">
                    <div class="report-title">研究方案</div>
                    <div class="report-meta">研究问题：{research_question}</div>
                </div>
                <div class="report-body">
                    {html_body}
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"研究方案生成失败：{e}")

elif start_btn and not research_question:
    st.markdown(
        '<div class="card-accent" style="font-size: 14px; color: #6B7280;">请输入研究问题以开始规划</div>',
        unsafe_allow_html=True,
    )

# ---- 空状态 ----
if not start_btn:
    st.markdown("""
    <div class="card-accent">
        <div class="guide-text">
            <strong>使用方式</strong><br>
            输入研究问题，系统将基于书籍方法论提供议题树拆解、数据源推荐、AI 工具建议与研究步骤规划。
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="margin-top: 16px;">
        <div class="guide-text"><strong>工具箱功能</strong></div>
        <table style="width: 100%; margin-top: 12px; font-size: 14px; border-collapse: collapse;">
            <tr><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600; width: 25%;">议题树生成</td><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">MECE 原则拆解研究问题</td></tr>
            <tr><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">数据源推荐</td><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">统计机构 / 研报 / 数据库 / 专家网络 / 另类数据</td></tr>
            <tr><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">AI 工具建议</td><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">适配研究阶段的 AI 工具推荐</td></tr>
            <tr><td style="padding: 8px 0; font-weight: 600;">研究步骤</td><td style="padding: 8px 0; color: #6B7280;">资讯料理法三阶段：备菜 &rarr; 烹饪 &rarr; 摆盘</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
