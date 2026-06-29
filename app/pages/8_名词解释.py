"""
名词解释 —— 行业研究术语速查
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.utils.style import inject_css
import markdown

st.set_page_config(page_title="名词解释 · 经纬", page_icon="◈", layout="wide")

inject_css()

st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">名词解释</h1>'
    '<div class="page-subtitle">'
    '行业研究术语速查 · 选自肖璟《如何快速了解一个行业》附录'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 搜索 ----
st.markdown('<div class="card">', unsafe_allow_html=True)
keyword = st.text_input(
    "输入术语关键词快速查找",
    placeholder="例如：渗透率、商业模式画布、护城河、PEST...",
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)

# 加载术语表
glossary_path = os.path.join(
    os.path.dirname(__file__), "..", "..", "knowledge-base", "glossary.md"
)

with open(glossary_path, encoding="utf-8") as f:
    raw = f.read()

# 按 ## 和 ** 解析术语条目
parsed = []
current_category = ""
for line in raw.split("\n"):
    line = line.strip()
    if line.startswith("## ") and not line.startswith("### "):
        current_category = line[3:].strip()
    elif line.startswith("**") and "**" in line[4:] and current_category:
        # 匹配 **术语**：解释
        parts = line.split("**")
        if len(parts) >= 3:
            term = parts[1].strip()
            definition = parts[2].strip().lstrip("：:").strip()
            if term and definition and len(term) < 80:
                parsed.append({
                    "category": current_category,
                    "term": term,
                    "definition": definition,
                })

# 筛选
if keyword:
    kw = keyword.lower()
    filtered = [t for t in parsed if kw in t["term"].lower() or kw in t["definition"].lower()]
else:
    filtered = parsed

if not keyword and not filtered:
    st.markdown(
        '<div class="card" style="text-align: center; padding: 48px;">'
        '<div style="color: #6B7280;">术语表加载中…</div></div>',
        unsafe_allow_html=True,
    )
elif keyword and not filtered:
    st.markdown(
        '<div class="card" style="text-align: center; padding: 48px;">'
        f'<div style="color: #6B7280;">未找到包含「{keyword}」的术语</div></div>',
        unsafe_allow_html=True,
    )
else:
    # 按类别分组
    from collections import OrderedDict
    grouped = OrderedDict()
    for t in filtered:
        grouped.setdefault(t["category"], []).append(t)

    for cat, terms in grouped.items():
        st.markdown(
            f'<div style="font-family: Georgia, serif; font-size: 16px; font-weight: 600; '
            f'color: #2C3338; margin-top: 24px; margin-bottom: 8px;">{cat}</div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(2)
        for i, t in enumerate(terms):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="module-card" style="padding: 12px 16px;">
                    <div style="font-size: 15px; font-weight: 600; color: #2D5A4B;">{t["term"]}</div>
                    <div style="font-size: 13px; color: #6B7280; margin-top: 4px; line-height: 1.6;">{t["definition"]}</div>
                </div>
                """, unsafe_allow_html=True)

st.markdown(
    '<div style="font-size: 13px; color: #9CA3AF; margin-top: 24px;">'
    '来源：肖璟《如何快速了解一个行业》(2025) 附录·328-331页'
    '</div>',
    unsafe_allow_html=True,
)
