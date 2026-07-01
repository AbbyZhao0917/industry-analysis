"""
智能分析 —— 统一入口，一个搜索框覆盖行业/企业/对比分析
"""
import sys, os, re
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import markdown
import streamlit as st
from app.services.claude_client import ask_claude
from app.utils.knowledge import build_system_context
from app.utils.style import inject_css
from app.utils.search import search_web
from app.utils.chart import parse_charts, embed_charts

st.set_page_config(page_title="智能分析 · 经纬", page_icon="◈", layout="wide")

inject_css()

# ---- 页面标题 ----
st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">智能分析</h1>'
    '<div class="page-subtitle">行业洞察 &middot; 企业深度 &middot; 对比分析 一框搞定</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 工具函数 ----
def parse_query(query: str):
    """解析输入，返回 (mode, entity_a, entity_b, display_title)"""
    query = query.strip()
    vs_pattern = re.split(r'\s+(?:vs\.?|VS\.?|Vs\.?)\s+', query)
    if len(vs_pattern) == 2:
        a, b = vs_pattern[0].strip(), vs_pattern[1].strip()
        return ("comparison", a, b, f"{a} vs {b}")
    else:
        return ("single", query, None, query)


def current_year() -> str:
    return str(datetime.now().year)


def save_report(display_title: str, content: str):
    """将报告保存到 reports/ 目录"""
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "..", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    safe_name = re.sub(r'[\\/:*?"<>|]', '_', display_title)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{safe_name}-{timestamp}.md"
    filepath = os.path.join(reports_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


# ---- 输入区 ----
st.markdown('<div class="search-hero">', unsafe_allow_html=True)

query = st.text_input(
    "search_query",
    placeholder="输入行业或企业名称，对比分析请用 vs 隔开（如：瑞幸 vs 星巴克）",
    label_visibility="collapsed",
    key="main_search",
)

st.markdown(
    '<div class="search-hints">'
    '<span>试试：</span>'
    '<code>现制茶饮</code> <span>·</span> '
    '<code>盒马</code> <span>·</span> '
    '<code>瑞幸 vs 星巴克</code> <span>·</span> '
    '<code>咖啡行业 vs 茶饮行业</code> <span>·</span> '
    '<code>蜜雪冰城 vs 现制茶饮</code>'
    '</div>',
    unsafe_allow_html=True,
)

start_btn = st.button("开始分析", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)


# ---- 构建 prompt ----
def build_prompt(mode: str, a: str, b: str) -> str:
    kb_names = [
        "business-model-canvas", "moat-framework", "competitive-analysis",
        "valuation-guide", "market-sizing", "industry-lifecycle",
        "pest-framework", "prosperity-tracking",
    ]
    system_prompt = build_system_context(kb_names)
    yr = current_year()

    if mode == "single":
        system_prompt += f"""

## 分析任务

分析对象：「{a}」

### 重要：请自行判断分析对象的类型
- 如果「{a}」是**行业**（如咖啡行业、新能源汽车），请按**七维度框架**展开：
  生命周期定位 → 可行性 → 规模性 → 防守性 → 盈利性 → 估值 → 外部因素(PEST) → 景气度
- 如果「{a}」是**企业**（如瑞幸、特斯拉），请按**企业分析框架**展开：
  企业概览与行业定位 → 商业模式画布（9要素） → UE单位经济模型 → 护城河评分卡（9项1-5分） → 竞争定位 → 估值框架 → 综合评估
- 如果不确定，按七维度分析，并在开头说明判断理由

### 数据时效性要求（极其重要）
- **当前年份是{yr}年**。所有数据必须优先使用{yr}年和{int(yr)-1}年的最新数据
- 如果搜索结果中只有旧数据（如2024年），请在报告中明确标注「最新可用数据截至20XX年」
- **每条数据必须用 Markdown 链接语法标注来源**：`[来源名称](完整URL)`
- 格式示例：「{yr}年市场规模5033亿元[（华经产业研究院）](https://www.huaon.com/channel/trend/1158078.html)」
- 搜索结果中标注的 URL 直接用于链接
- 不得使用"据XX机构数据"等模糊表述

### 图表要求
- 当有适合可视化的数据时，在报告中嵌入图表数据块：
```chart
{{"type": "bar", "title": "图表标题", "labels": ["2019","2020","2021"], "values": [100,200,300], "xlabel": "年份", "ylabel": "亿元"}}
```
- 支持的 type: bar（柱状图）、line（折线图）、pie（饼图）、radar（雷达图）
- labels 和 values 长度必须一致

### 格式要求
- 每个大段落用 ## 二级标题开头
- 全文第一个 ## 之前的内容作为概述（3-5句话即可）
- 使用表格展示数据对比，标注数据来源
- 中文输出
"""
    else:
        system_prompt += f"""

## 分析任务

对「{a}」和「{b}」进行对比分析。

### 重要：请自行判断分析对象的类型组合
- **行业 vs 行业** → 七维度并排对比
- **企业 vs 企业** → 商业模式画布、UE模型、护城河、估值、竞争定位 五大维度 PK
- **企业 vs 行业** 或 **行业 vs 企业** → 先分析企业在该行业中的定位与竞争地位，再展开行业全景分析，最后给出交叉对比结论

### 数据时效性要求（极其重要）
- **当前年份是{yr}年**。所有数据必须优先使用{yr}年和{int(yr)-1}年的最新数据
- 如果搜索结果中只有旧数据，请在报告中明确标注
- **每条数据必须用 Markdown 链接语法标注来源**：`[来源名称](完整URL)`

### 图表要求
- 当有适合可视化的对比数据时，嵌入图表：
```chart
{{"type": "bar", "title": "图表标题", "labels": ["指标1","指标2"], "values": [100,200], "xlabel": "", "ylabel": ""}}
```
- 对比场景优先使用 bar 展示差异

### 格式要求
- 每个大段落用 ## 二级标题开头，中文输出
"""

    return system_prompt


# ---- 搜索 + 生成 ----
def generate_report(mode: str, a: str, b: str, display_title: str) -> str:
    """执行分析，返回报告文本。异常返回 None。"""
    system_prompt = build_prompt(mode, a, b)
    yr = current_year()

    # 联网搜索（使用动态年份）
    search_query_a = a
    search_query_b = b if b else ""
    searching_label = f"正在联网搜索「{a}」" + (f"与「{b}」" if b else "") + "最新数据..."

    with st.spinner(searching_label):
        search_a = search_web(f"{search_query_a} 市场规模 行业报告 {yr}")
        search_b = ""
        if b:
            search_b = search_web(f"{search_query_b} 市场规模 行业报告 {yr}")

        search_block = f"## 联网搜索结果\n\n### {a}\n{search_a}"
        if b:
            search_block += f"\n\n### {b}\n{search_b}"
        system_prompt += f"\n\n{search_block}\n\n请基于以上搜索结果，结合方法论框架进行分析。优先使用搜索结果中的最新数据。"

    try:
        return ask_claude(system_prompt, f"请分析：{display_title}")
    except Exception as e:
        st.error(f"分析未能完成：{e}")
        return None


# ---- 渲染报告（左侧目录 + 右侧内容） ----
def display_report(response: str, display_title: str):
    """渲染已存储的报告"""
    sections = re.split(r'\n(?=## )', response)

    # 确保选中章节有效
    toc_key = f"toc_idx_{display_title}"
    if toc_key not in st.session_state:
        st.session_state[toc_key] = 0
    if st.session_state[toc_key] >= len(sections):
        st.session_state[toc_key] = 0

    # 报告头部
    st.markdown(f"""
    <div class="report-container">
        <div class="report-header">
            <div class="report-title">{display_title} 分析报告</div>
            <div class="report-meta">
                分析框架：七维度 + 商业模式画布 + 护城河 &middot;
                以下内容基于公开数据生成，仅供参考
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 左右分栏
    col_toc, col_content = st.columns([1, 3])

    with col_toc:
        st.markdown('<div class="toc-panel">', unsafe_allow_html=True)
        st.markdown('<div class="toc-title">报告目录</div>', unsafe_allow_html=True)

        for i, sec in enumerate(sections):
            title_line = sec.strip().split('\n')[0]
            title = title_line.lstrip('#').strip()
            display = title if len(title) <= 24 else title[:22] + "…"
            is_active = (i == st.session_state[toc_key])

            if st.button(display, key=f"toc_{display_title}_{i}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state[toc_key] = i
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_content:
        idx = st.session_state[toc_key]
        raw_section = sections[idx]
        html_body = markdown.markdown(raw_section, extensions=['tables', 'fenced_code'])
        html_body = embed_charts(html_body)
        st.markdown(f'<div class="report-body">{html_body}</div>', unsafe_allow_html=True)

    # 下载按钮
    st.download_button(
        label="下载 Markdown 报告",
        data=response,
        file_name=f"{display_title.replace(' ', '_')}_分析报告.md",
        mime="text/markdown",
    )


# ============================================================
# 核心流程：新查询 → 生成并存储 → 显示 | 已有报告 → 直接显示
# ============================================================

if start_btn and query:
    # 新查询：生成报告
    mode, a, b, display_title = parse_query(query)

    response = generate_report(mode, a, b, display_title)

    if response:
        # 存储到 session_state，确保 rerun 后不丢失
        st.session_state["report_response"] = response
        st.session_state["report_title"] = display_title
        st.session_state["report_query"] = query

        # 自动存档到 reports/ 目录
        saved_path = save_report(display_title, response)
        st.toast(f"报告已自动存档", icon="📄")

        # 重置 TOC 选中章节
        st.session_state[f"toc_idx_{display_title}"] = 0

        st.rerun()

elif start_btn and not query:
    st.markdown(
        '<div class="card-accent" style="font-size: 14px; color: #6B7280;">请输入行业或企业名称以开始分析</div>',
        unsafe_allow_html=True,
    )

# ---- 显示已存储的报告 ----
if "report_response" in st.session_state and st.session_state["report_response"]:
    display_report(st.session_state["report_response"], st.session_state["report_title"])

# ---- 空状态 ----
if "report_response" not in st.session_state or not st.session_state.get("report_response"):
    if not start_btn:
        st.markdown("""
        <div class="card-accent" style="margin-top: 20px;">
            <div class="guide-text">
                <strong>智能分析能力</strong><br>
                输入任意行业或企业名称，系统自动判断分析对象类型、选择适配框架。<br>
                对比分析用 <code>vs</code> 隔开两个对象，支持 行业vs行业、企业vs企业、企业vs行业 三种模式。
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="card" style="margin-top: 16px;">
                <div class="guide-text"><strong>行业分析维度</strong></div>
                <table style="width: 100%; margin-top: 12px; font-size: 14px; border-collapse: collapse;">
                    <tr><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">生命周期定位</td><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">导入 / 成长 / 成熟 / 衰退</td></tr>
                    <tr><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">可行性 · 规模性</td><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">商业模式 + 市场天花板</td></tr>
                    <tr><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">防守性 · 盈利性</td><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">护城河 + 利润分配</td></tr>
                    <tr><td style="padding: 6px 0; font-weight: 600;">估值 · 外部 · 景气度</td><td style="padding: 6px 0; color: #6B7280;">估值框架 + PEST + 行业温度</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="card" style="margin-top: 16px;">
                <div class="guide-text"><strong>企业分析维度</strong></div>
                <table style="width: 100%; margin-top: 12px; font-size: 14px; border-collapse: collapse;">
                    <tr><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">企业概览</td><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">行业定位 + 竞争格局</td></tr>
                    <tr><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">商业模式画布</td><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">9 要素完整填写</td></tr>
                    <tr><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; font-weight: 600;">UE 模型</td><td style="padding: 6px 0; border-bottom: 1px solid #E2E0DA; color: #6B7280;">单店 / 单客收入-成本-利润</td></tr>
                    <tr><td style="padding: 6px 0; font-weight: 600;">护城河 · 估值</td><td style="padding: 6px 0; color: #6B7280;">9项评分 + 可比公司分析</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
