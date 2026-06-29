"""
知识库浏览器 —— 浏览 12个方法论知识库文件
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.utils.knowledge import list_knowledge_files, load_knowledge

st.set_page_config(page_title="知识库", page_icon="📚", layout="wide")

st.title("📚 知识库浏览器")
st.caption("肖璟《如何快速了解一个行业》方法论知识库 · 12个模块")

kb_files = list_knowledge_files()
if not kb_files:
    st.warning("未找到知识库文件，请确认 knowledge-base/ 目录存在")
else:
    # 中文标题映射
    title_map = {
        "ai-research-guide": "🤖 AI辅助研究指南",
        "business-model-canvas": "📋 商业模式画布与可行性分析",
        "competitive-analysis": "⚔️ 竞争格局与盈利性分析",
        "data-sources": "📊 研究数据源大全",
        "glossary": "📖 行业研究术语表",
        "industry-lifecycle": "🔄 产业生命周期框架",
        "market-sizing": "📐 市场规模测算",
        "moat-framework": "🛡️ 护城河框架",
        "pest-framework": "🌍 PEST外部因素分析",
        "prosperity-tracking": "📡 景气度跟踪框架",
        "research-cookbook": "🍳 资讯料理法与研究输出",
        "valuation-guide": "💰 估值指南",
    }

    selected = st.selectbox(
        "选择知识库模块",
        kb_files,
        format_func=lambda x: title_map.get(x, x),
    )

    if selected:
        content = load_knowledge(selected)
        if content:
            st.markdown(f"## {title_map.get(selected, selected)}")
            st.markdown(content)
        else:
            st.warning("文件内容为空")