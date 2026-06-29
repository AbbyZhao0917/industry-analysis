"""
报告中心 —— 历史分析记录归档
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.utils.style import inject_css

st.set_page_config(page_title="报告中心 · 经纬", page_icon="◈", layout="wide")

inject_css()

st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">报告中心</h1>'
    '<div class="page-subtitle">历史分析记录归档</div>'
    '</div>',
    unsafe_allow_html=True,
)

reports_dir = os.path.join(os.path.dirname(__file__), "..", "..", "reports")

if os.path.isdir(reports_dir):
    files = sorted(
        [f for f in os.listdir(reports_dir) if f.endswith(".md")],
        reverse=True,
    )

    if not files:
        st.markdown(
            '<div class="card" style="text-align: center; padding: 48px 24px;">'
            '<div style="font-size: 15px; color: #6B7280;">暂无存档报告</div>'
            '<div style="font-size: 13px; color: #9CA3AF; margin-top: 8px;">'
            '在"行业分析"或"企业分析"模块中生成的报告将自动存档于此</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        for f in files:
            filepath = os.path.join(reports_dir, f)
            with open(filepath) as fp:
                content = fp.read()

            # Extract title from first H1 line
            title = f.replace(".md", "")
            preview = content[:200].strip().replace("\n", " ") + "..."

            with st.expander(title):
                st.markdown(content)
else:
    st.markdown(
        '<div class="card" style="text-align: center; padding: 48px 24px;">'
        '<div style="font-size: 15px; color: #6B7280;">报告存档目录未创建</div>'
        '</div>',
        unsafe_allow_html=True,
    )
