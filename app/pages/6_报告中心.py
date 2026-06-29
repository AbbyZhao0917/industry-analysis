"""
报告中心 —— 历史分析记录 · 模板管理 · 报告导出
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st

st.set_page_config(page_title="报告中心", page_icon="📋", layout="wide")

st.title("📋 报告中心")
st.caption("历史分析记录 · 模板管理 · 报告导出")

st.info("🚧 报告中心功能开发中...")

# 报告存档展示
reports_dir = os.path.join(os.path.dirname(__file__), "..", "..", "reports")
if os.path.isdir(reports_dir):
    st.subheader("已存档的分析报告")
    for f in sorted(os.listdir(reports_dir), reverse=True):
        if f.endswith(".md"):
            filepath = os.path.join(reports_dir, f)
            with st.expander(f"📄 {f}"):
                with open(filepath, "r") as fp:
                    st.markdown(fp.read())