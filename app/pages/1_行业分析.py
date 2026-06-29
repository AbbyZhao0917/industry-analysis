"""
行业分析 —— 七维度框架 · 结构化研究报告
"""
import sys
import os
import markdown

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context
from app.utils.style import inject_css
from app.utils.search import search_for_industry

st.set_page_config(page_title="行业分析 · 经纬", page_icon="◈", layout="wide")

inject_css()

st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">行业分析</h1>'
    '<div class="page-subtitle">'
    '按七维度框架输出结构化研究报告 &middot; 数据来源标注 URL'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 输入区 ----
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    industry_name = st.text_input(
        "输入行业名称",
        placeholder="例如：预制菜、便利店、CPO、新能源车、银发经济...",
        label_visibility="collapsed",
    )
with col2:
    analysis_depth = st.selectbox(
        "分析深度",
        ["标准（3000-5000字）", "精简（1500字）", "深度（8000字+）"],
        label_visibility="collapsed",
    )
with col3:
    start_btn = st.button("开始分析", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---- 分析执行 ----
if start_btn and industry_name:
    kb_names = [
        "industry-lifecycle", "business-model-canvas", "market-sizing",
        "moat-framework", "competitive-analysis", "valuation-guide",
        "pest-framework", "prosperity-tracking", "research-cookbook", "data-sources",
    ]
    system_prompt = build_system_context(kb_names)
    system_prompt += f"""

## 分析任务

对「{industry_name}」行业进行完整的七维度分析。

### 要求
1. 先搜索最新数据（市场规模、渗透率、政策、头部公司财报），每条数据标注具体来源URL和时间
2. 判断产业生命周期阶段（渗透率法 + 辅助信号）
3. 七维度逐一分析，根据生命周期阶段调整权重
4. 使用 SCQR 格式输出（情境→冲突→问题→方案）
5. 中文输出，分析深度：{analysis_depth}

### 数据来源强制要求
- 每条数据必须包含具体网址（URL），不得只写"XXX报告"或"XXX研究院"
- 格式示例：「2025年市场规模5033亿元（来源：https://www.huaon.com/channel/trend/1158078.html，华经产业研究院，2025）」
- 优先使用书中推荐的资源：国家统计局、行业协会官网、券商研报、专业数据库、公司招股书/年报
"""

    # 联网搜索最新数据
    search_results = search_for_industry(industry_name)
    system_prompt += f"\n\n## 联网搜索结果（最新公开数据）\n\n{search_results}\n\n请基于以上搜索结果，结合方法论框架进行分析。"

    with st.spinner(f"正在联网搜索「{industry_name}」行业最新数据并执行分析..."):
        try:
            response = ask_claude(system_prompt, f"请分析「{industry_name}」行业")

            html_body = markdown.markdown(response, extensions=['tables', 'fenced_code'])
            st.markdown(f"""
            <div class="report-container">
                <div class="report-header">
                    <div class="report-title">{industry_name} 行业研究报告</div>
                    <div class="report-meta">
                        分析框架：七维度 &middot; 分析深度：{analysis_depth} &middot;
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

elif start_btn and not industry_name:
    st.markdown(
        '<div class="card-accent" style="font-size: 14px; color: #6B7280;">请输入行业名称以开始分析</div>',
        unsafe_allow_html=True,
    )

# ---- 空状态 ----
if not start_btn:
    st.markdown("""
    <div class="card-accent">
        <div class="guide-text">
            <strong>使用方式</strong><br>
            输入行业名称，系统将自动检索最新公开数据，按七维度框架输出结构化研究报告。<br>
            每条数据均标注来源 URL 与时间。
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="margin-top: 16px;">
        <div class="guide-text">
            <strong>分析维度</strong>
        </div>
        <table style="width: 100%; margin-top: 12px; font-size: 14px; border-collapse: collapse;">
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600; width: 25%;">可行性</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">商业模式画布 + 对标法 + UE模型</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">规模性</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">TAM/SAM/SOM + 市场规模测算</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">防守性</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">护城河9子项评分卡</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">盈利性</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">CRn集中度 + 五力模型 + 产业链利润分配</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">估值</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">生命周期对应估值方法</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">外部因素</td>
                <td style="padding: 8px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">PEST四维分析 + 技术创新金字塔</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; font-weight: 600;">景气度</td>
                <td style="padding: 8px 0; color: #6B7280;">关键指标识别 + 当前景气度判断</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
