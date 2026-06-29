"""
企业对比 —— 双企业并排 PK
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import markdown
import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context
from app.utils.style import inject_css

st.set_page_config(page_title="企业对比 · 经纬", page_icon="◈", layout="wide")

inject_css()

st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">企业对比</h1>'
    '<div class="page-subtitle">商业模式画布 &middot; UE 指标 &middot; 护城河评分 &middot; 估值 逐项 PK</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 输入区 ----
st.markdown('<div class="card">', unsafe_allow_html=True)
col_a, col_b = st.columns(2)
with col_a:
    company_a = st.text_input("企业 A", placeholder="例如：盒马", label_visibility="collapsed")
with col_b:
    company_b = st.text_input("企业 B", placeholder="例如：叮咚买菜", label_visibility="collapsed")
start_btn = st.button("开始对比", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---- 分析执行 ----
if start_btn and company_a and company_b:
    kb_names = ["business-model-canvas", "moat-framework", "competitive-analysis", "valuation-guide"]
    system_prompt = build_system_context(kb_names)
    system_prompt += f"""

## 分析任务

对「{company_a}」和「{company_b}」进行并排对比分析。

### 对比维度
1. 商业模式画布PK（9要素并排表）
2. UE模型关键指标PK（客单价、毛利率、净利率、回本周期等）
3. 护城河评分PK（9子项逐项评分 + 总分）
4. 竞争定位对比
5. 估值对比

### 最终输出
- 维度胜负统计（各赢几个维度）
- 各自优势场景
- 核心差异总结
- 选择建议

### 数据来源强制要求
每条数据必须标注具体来源URL和时间
"""

    with st.spinner(f"正在检索「{company_a}」与「{company_b}」公开数据并执行对比分析..."):
        try:
            response = ask_claude(system_prompt, f"请对比分析「{company_a}」和「{company_b}」两家企业")
            html_body = markdown.markdown(response, extensions=['tables', 'fenced_code'])

            st.markdown(f"""
            <div class="report-container">
                <div class="report-header">
                    <div class="report-title">{company_a} vs {company_b} &middot; 企业对比</div>
                    <div class="report-meta">
                        对比框架：商业模式画布 + UE模型 + 护城河 + 估值 &middot;
                        以下内容基于公开数据生成，仅供参考
                    </div>
                </div>
                <div class="report-body">
                    {html_body}
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"分析未能完成：{e}")

elif start_btn and not (company_a and company_b):
    st.markdown(
        '<div class="card-accent" style="font-size: 14px; color: #6B7280;">请输入两家企业名称以开始对比</div>',
        unsafe_allow_html=True,
    )

# ---- 空状态 ----
if not start_btn:
    st.markdown("""
    <div class="card-accent">
        <div class="guide-text">
            <strong>使用方式</strong><br>
            输入两家企业名称，系统将自动检索最新公开数据，按五大维度并排对比分析，输出维度胜负统计与选择建议。
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="margin-top: 16px;">
        <div class="guide-text"><strong>对比维度</strong></div>
        <table style="width: 100%; margin-top: 12px; font-size: 14px; border-collapse: collapse;">
            <tr><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600; width: 25%;">商业模式画布</td><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">9 要素并排对比</td></tr>
            <tr><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">UE 模型指标</td><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">客单价 / 毛利率 / 净利率 / 回本周期</td></tr>
            <tr><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">护城河 PK</td><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">9 项评分 1-5 逐项对比</td></tr>
            <tr><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">竞争定位</td><td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">市场份额 / 产业链议价力</td></tr>
            <tr><td style="padding: 8px 0; font-weight: 600;">估值对比</td><td style="padding: 8px 0; color: #6B7280;">PE / PB / PS + 估值水位判断</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
