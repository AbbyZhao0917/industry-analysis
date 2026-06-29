"""
行业对比 —— 双行业七维度并排分析
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context
from app.utils.style import inject_css

st.set_page_config(page_title="行业对比 · 经纬", page_icon="◈", layout="wide")

inject_css()

st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">行业对比</h1>'
    '<div class="page-subtitle">两个行业七维度并排对比 &middot; 差异高亮 &middot; 选择建议</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 输入区 ----
st.markdown('<div class="card">', unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    industry_a = st.text_input("行业 A", placeholder="例如：生鲜电商", label_visibility="collapsed")
with col_b:
    industry_b = st.text_input("行业 B", placeholder="例如：社区团购", label_visibility="collapsed")
start_btn = st.button("开始对比", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---- 分析执行 ----
if start_btn and industry_a and industry_b:
    kb_names = [
        "industry-lifecycle", "business-model-canvas", "market-sizing",
        "moat-framework", "competitive-analysis", "valuation-guide",
        "pest-framework", "prosperity-tracking",
    ]
    system_prompt = build_system_context(kb_names)
    system_prompt += f"""

## 分析任务

对「{industry_a}」和「{industry_b}」两个行业进行七维度并排对比。

### 要求
1. 分别定位两个行业的生命周期阶段
2. 七维度逐一并排对比：可行性/规模性/防守性/盈利性/估值/外部因素/景气度
3. 每个维度呈现两个行业的最新数据（标注来源URL和时间）
4. 差异高亮 + 选择矩阵（成长性/确定性/长期价值角度）
5. 综合建议 + 风险提示

### 数据来源强制要求
每条数据必须标注具体来源URL和时间
"""

    with st.spinner(f"正在检索「{industry_a}」与「{industry_b}」行业公开数据并执行对比分析..."):
        try:
            response = ask_claude(system_prompt, f"请对比分析「{industry_a}」和「{industry_b}」两个行业")

            st.markdown(f"""
            <div class="report-container">
                <div class="report-header">
                    <div class="report-title">{industry_a} vs {industry_b} &middot; 行业对比</div>
                    <div class="report-meta">
                        分析框架：七维度并排对比 &middot;
                        以下内容基于公开数据生成，仅供参考
                    </div>
                </div>
                <div class="report-body">
                    {response}
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"分析未能完成：{e}")

elif start_btn and not (industry_a and industry_b):
    st.markdown(
        '<div class="card-accent" style="font-size: 14px; color: #6B7280;">请输入两个行业名称以开始对比</div>',
        unsafe_allow_html=True,
    )

# ---- 空状态 ----
if not start_btn:
    st.markdown("""
    <div class="card-accent">
        <div class="guide-text">
            <strong>使用方式</strong><br>
            输入两个行业名称，系统将自动检索最新公开数据，按七维度并排对比，输出差异分析与选择建议。
        </div>
    </div>
    """, unsafe_allow_html=True)
