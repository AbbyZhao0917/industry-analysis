"""加载全局 CSS。从各页面调用。"""
import os
import streamlit as st


def inject_css():
    """将 style.css 注入到当前页面"""
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
    if not os.path.exists(css_path):
        return
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
