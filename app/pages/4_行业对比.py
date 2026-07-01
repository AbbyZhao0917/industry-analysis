"""
行业对比 —— 双行业七维度并排分析
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import markdown
import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context
from app.utils.style import inject_css
from app.utils.search import search_for_industry

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
col_a, col_b = st.columns(2)
with col_a:
    industry_a = st.text_input("行业 A", placeholder="例如：生鲜电商", label_visibility="collapsed")
with col_b:
    industry_b = st.text_input("行业 B", placeholder="例如：社区团购", label_visibility="collapsed")
start_btn = st.button("开始对比", type="primary", use_container_width=True)

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

### 数据来源强制要求（极其重要）
- **每条数据必须用 Markdown 链接语法标注来源**：`[来源名称](完整URL)`
- 格式示例：「2025年市场规模5033亿元[（华经产业研究院）](https://www.huaon.com/channel/trend/1158078.html)」
- 搜索结果中标注的 URL 直接用于链接
- 不得使用"据XX机构数据"等模糊表述，必须给出可点击链接
- 优先使用书中推荐的资源类型：统计机构官网、行业协会官网、券商研报、公司招股书/年报
"""

    # 联网搜索最新数据
    search_results_a = search_for_industry(industry_a)
    search_results_b = search_for_industry(industry_b)
    system_prompt += f"\n\n## 联网搜索结果（最新公开数据）\n\n### {industry_a}\n\n{search_results_a}\n\n### {industry_b}\n\n{search_results_b}\n\n请基于以上搜索结果，结合方法论框架进行分析。"

    with st.spinner(f"正在联网搜索「{industry_a}」与「{industry_b}」行业最新数据..."):
        try:
            response = ask_claude(system_prompt, f"请对比分析「{industry_a}」和「{industry_b}」两个行业")
            import re

            # 按 H2 标题拆分
            sections = re.split(r'\n(?=## )', response)

            # 报告容器开头
            st.markdown(f"""
            <div class="report-container">
                <div class="report-header">
                    <div class="report-title">{industry_a} vs {industry_b} &middot; 行业对比</div>
                    <div class="report-meta">
                        分析框架：七维度并排对比 &middot;
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
                file_name=f"{industry_a}_vs_{industry_b}_对比报告.md",
                mime="text/markdown",
            )

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
