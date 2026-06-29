"""
知识库浏览器 —— 12 个方法论模块
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.utils.knowledge import list_knowledge_files, load_knowledge
from app.utils.style import inject_css

st.set_page_config(page_title="知识库 · 经纬", page_icon="◈", layout="wide")

inject_css()

st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">知识库</h1>'
    '<div class="page-subtitle">肖璟《如何快速了解一个行业》(2025) 方法论体系 &middot; 12 个模块</div>'
    '</div>',
    unsafe_allow_html=True,
)

kb_files = list_knowledge_files()
if not kb_files:
    st.markdown(
        '<div class="card-accent" style="font-size: 14px; color: #6B7280;">'
        '未找到知识库文件，请确认 knowledge-base/ 目录存在</div>',
        unsafe_allow_html=True,
    )
else:
    title_map = {
        "ai-research-guide": "AI 辅助研究指南",
        "business-model-canvas": "商业模式画布与可行性分析",
        "competitive-analysis": "竞争格局与盈利性分析",
        "data-sources": "研究数据源大全",
        "glossary": "行业研究术语表",
        "industry-lifecycle": "产业生命周期框架",
        "market-sizing": "市场规模测算",
        "moat-framework": "护城河框架",
        "pest-framework": "PEST 外部因素分析",
        "prosperity-tracking": "景气度跟踪框架",
        "research-cookbook": "资讯料理法与研究输出",
        "valuation-guide": "估值指南",
    }

    # Select module
    st.markdown('<div class="card">', unsafe_allow_html=True)
    selected = st.selectbox(
        "选择知识库模块",
        kb_files,
        format_func=lambda x: title_map.get(x, x),
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if selected:
        content = load_knowledge(selected)
        if content:
            module_title = title_map.get(selected, selected)
            st.markdown(f"""
            <div class="report-container">
                <div class="report-header">
                    <div class="report-title">{module_title}</div>
                    <div class="report-meta">知识库模块 &middot; 方法论来源：肖璟 (2025)</div>
                </div>
                <div class="report-body">
                    {content}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="card-accent" style="font-size: 14px; color: #6B7280;">文件内容为空</div>',
                unsafe_allow_html=True,
            )
