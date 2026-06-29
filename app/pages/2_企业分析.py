"""
企业分析 —— 商业模式画布 · UE模型 · 护城河评分
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context
from app.utils.style import inject_css

st.set_page_config(page_title="企业分析 · 经纬", page_icon="◈", layout="wide")

inject_css()

st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">企业分析</h1>'
    '<div class="page-subtitle">商业模式画布 &middot; UE 单位经济模型 &middot; 护城河评分卡 &middot; 估值框架</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 输入区 ----
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    company_name = st.text_input(
        "输入企业名称",
        placeholder="例如：明康汇、盒马、见福便利店...",
        label_visibility="collapsed",
    )
with col2:
    depth = st.selectbox(
        "分析深度",
        ["标准", "精简", "深度"],
        label_visibility="collapsed",
    )
with col3:
    start_btn = st.button("开始分析", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---- 分析执行 ----
if start_btn and company_name:
    kb_names = [
        "business-model-canvas", "moat-framework", "competitive-analysis",
        "valuation-guide", "market-sizing",
    ]
    system_prompt = build_system_context(kb_names)
    system_prompt += f"""

## 分析任务

对「{company_name}」进行深度企业分析。分析深度：{depth}。

### 要求
1. 先搜索企业最新数据（财报/业务/竞争），每条数据标注具体来源URL和时间
2. 绘制商业模式画布（9要素完整填写）
3. 构建UE单位经济模型（填入具体数字或推估值并标注）
4. 护城河评分卡（9子项逐一评分1-5，每项给出理由）
5. 竞争定位 + 估值框架
6. 中文输出

### 数据来源强制要求
- 每条数据必须包含具体网址（URL）
- 格式：「营收382亿（来源：https://stock.finance.sina.com.cn/...，2025年报）」
"""

    with st.spinner(f"正在检索「{company_name}」公开数据并执行结构分析..."):
        try:
            response = ask_claude(system_prompt, f"请分析「{company_name}」企业")

            st.markdown(f"""
            <div class="report-container">
                <div class="report-header">
                    <div class="report-title">{company_name} 企业分析报告</div>
                    <div class="report-meta">
                        分析框架：商业模式画布 + UE模型 + 护城河评分 &middot;
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

elif start_btn and not company_name:
    st.markdown(
        '<div class="card-accent" style="font-size: 14px; color: #6B7280;">请输入企业名称以开始分析</div>',
        unsafe_allow_html=True,
    )

# ---- 空状态 ----
if not start_btn:
    st.markdown("""
    <div class="card-accent">
        <div class="guide-text">
            <strong>使用方式</strong><br>
            输入企业名称，系统将自动检索最新公开数据，输出商业模式画布、UE 单位经济模型、护城河评分卡与估值框架。
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="margin-top: 16px;">
        <div class="guide-text">
            <strong>分析内容</strong>
        </div>
        <table style="width: 100%; margin-top: 12px; font-size: 14px; border-collapse: collapse;">
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600; width: 30%;">企业概览与行业定位</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">生命周期阶段 + 行业竞争格局</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">商业模式画布</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">9 要素完整填写</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">UE 单位经济模型</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">单店/单客收入-成本-利润结构</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">护城河评分卡</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">9 子项逐一评分 1-5 </td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">竞争定位与估值</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">可比公司分析 + 估值水位判断</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; font-weight: 600;">综合评估</td>
                <td style="padding: 8px 0; color: #6B7280;">投资亮点 + 风险提示</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
