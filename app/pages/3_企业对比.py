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
from app.utils.search import search_for_company

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
col_a, col_b = st.columns(2)
with col_a:
    company_a = st.text_input("企业 A", placeholder="例如：盒马", label_visibility="collapsed")
with col_b:
    company_b = st.text_input("企业 B", placeholder="例如：叮咚买菜", label_visibility="collapsed")
start_btn = st.button("开始对比", type="primary", use_container_width=True)

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

### 数据来源强制要求（极其重要）
- **每条数据必须用 Markdown 链接语法标注来源**：`[来源名称](完整URL)`
- 格式示例：「2025年营收382亿[（公司年报）](https://example.com)」
- 搜索结果中标注的 URL 直接用于链接
- 不得使用"据XX机构数据"等模糊表述，必须给出可点击链接
- 优先使用书中推荐的资源类型：统计机构官网、行业协会官网、券商研报、公司招股书/年报
"""

    # 联网搜索最新数据
    search_results_a = search_for_company(company_a)
    search_results_b = search_for_company(company_b)
    system_prompt += f"\n\n## 联网搜索结果（最新公开数据）\n\n### {company_a}\n\n{search_results_a}\n\n### {company_b}\n\n{search_results_b}\n\n请基于以上搜索结果，结合方法论框架进行分析。"

    with st.spinner(f"正在联网搜索「{company_a}」与「{company_b}」最新数据..."):
        try:
            response = ask_claude(system_prompt, f"请对比分析「{company_a}」和「{company_b}」两家企业")
            import re

            # 按 H2 标题拆分
            sections = re.split(r'\n(?=## )', response)

            # 报告容器开头
            st.markdown(f"""
            <div class="report-container">
                <div class="report-header">
                    <div class="report-title">{company_a} vs {company_b} &middot; 企业对比</div>
                    <div class="report-meta">
                        对比框架：商业模式画布 + UE模型 + 护城河 + 估值 &middot;
                        以下内容基于公开数据生成，仅供参考
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 第一段是概述，直接展示
            if sections:
                first = markdown.markdown(sections[0], extensions=['tables', 'fenced_code'])
                st.markdown(f'<div class="report-body">{first}</div>', unsafe_allow_html=True)

            # 后续每段一个 expander
            for sec in sections[1:]:
                title_line = sec.strip().split('\n')[0]
                title = title_line.lstrip('#').strip()
                body_html = markdown.markdown(sec, extensions=['tables', 'fenced_code'])
                with st.expander(title, expanded=False):
                    st.markdown(f'<div class="report-body" style="margin-top: -12px;">{body_html}</div>', unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button(
                label="下载 Markdown 报告",
                data=response,
                file_name=f"{company_a}_vs_{company_b}_对比报告.md",
                mime="text/markdown",
            )

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
