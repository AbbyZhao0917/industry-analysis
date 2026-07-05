"""
经纬 · 行业洞察 —— 基于肖璟《如何快速了解一个行业》方法论
"""
import sys, os, re
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import markdown
import streamlit as st
from app.services.claude_client import ask_claude, ask_claude_stream
from app.utils.knowledge import build_system_context
from app.utils.style import inject_css
from app.utils.search import search_by_dimensions, search_authoritative
from app.utils.chart import parse_charts, embed_charts

st.set_page_config(page_title="经纬 · 行业洞察", page_icon="◈", layout="wide")

inject_css()

# ---- 页面标题 ----
st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">经纬 · 行业洞察</h1>'
    '<div class="page-subtitle">基于产业生命周期主线的七维度分析框架<br>输入行业或企业名称，自动检索最新公开数据，输出结构化研究报告</div>'
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
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
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
        "pest-framework", "prosperity-tracking", "data-sources",
    ]
    system_prompt = build_system_context(kb_names)
    yr = current_year()

    if mode == "single":
        system_prompt += f"""

## 分析任务

分析对象：「{a}」

### 重要：请自行判断分析对象的类型
- 如果「{a}」是**行业**（如咖啡行业、新能源汽车），请按**七维度框架**展开，每个维度用 `##` 二级标题：
  `## 生命周期定位` → `## 可行性` → `## 规模性` → `## 防守性` → `## 盈利性` → `## 估值` → `## 外部因素(PEST)` → `## 景气度`
- 如果「{a}」是**企业**（如瑞幸、特斯拉），请按**企业分析框架**展开，每个模块用 `##` 二级标题：
  `## 企业概览与行业定位` → `## 商业模式画布`（9要素表格） → `## UE单位经济模型` → `## 护城河评分卡`（9项1-5分） → `## 竞争定位` → `## 估值框架` → `## 综合评估`
- 如果不确定，按七维度分析，并在开头说明判断理由

### 数据来源规则（极其重要）
**你必须从知识库「data-sources」中列出的权威渠道获取数据，按优先级排序：**

1. **官方统计机构**：国家统计局（stats.gov.cn）、行业协会（如CCFA、中国烹饪协会、中汽协等）、央行、海关总署
2. **公司公开文件**：招股书（最重要！免费且数据最详实）、年报/季报、投资者演示材料
3. **券商研究报告**：中金、中信、华泰等（可通过东方财富 eastmoney.com 免费获取）
4. **咨询公司报告**：艾瑞、亿欧、麦肯锡、BCG、德勤等
5. **专业数据库**：Wind、Euromonitor、Statista、IT桔子

**引用格式规则：**
- 每条数据后紧跟 `[（来源名称）](URL)`，URL 直接来自搜索结果中的链接
- 搜索结果中包含了「权威源定向检索」结果（国家统计局、巨潮资讯招股书/年报、艾瑞报告、东方财富研报、行业协会等），**必须优先引用这些权威来源**
- **禁止使用"未能获取""搜索能力限制"等消极表述**——搜索结果中已有的权威数据就直接使用，不要标注为缺失
- 示例：「2025年餐饮市场规模5.2万亿元[（中国烹饪协会）](https://www.ccas.com.cn/...)」
- 严禁使用"据XX机构数据"等模糊表述——必须有 URL

### 数据时效性要求
- **当前年份是{yr}年**。所有数据必须优先使用{yr}年和{int(yr)-1}年的最新数据
- 如果搜索结果中只有旧数据（如2024年），请在报告中明确标注「最新可用数据截至20XX年」

### 📋 合规要求（新增栏目）
- 在报告末尾增加独立的「## 合规要求」章节
- 列出该行业/企业需要遵守的**现行有效的**政策法规和标准
- 每条法规需包含：**名称、发布单位、发布时间/最新修订时间、全文链接（如有）**
- 分类建议：国家法律、行政法规、部门规章、行业标准、国际标准
- 如果搜索结果中缺乏具体法规信息，列出应关注的监管方向并标注「需进一步核实」

### 图表要求
- 当有适合可视化的数据时，在报告中嵌入图表数据块：
```chart
{{"type": "bar", "title": "图表标题", "labels": ["2019","2020","2021"], "values": [100,200,300], "xlabel": "年份", "ylabel": "亿元"}}
```
- 支持的 type: bar（柱状图）、line（折线图）、pie（饼图）、radar（雷达图）
- labels 和 values 长度必须一致，JSON 必须完整闭合
- **图表 JSON 必须严格合法**：所有括号配对、字符串闭合、不含注释

### 格式要求
- 每个大段落用 ## 二级标题开头
- 全文第一个 ## 之前的内容作为概述（3-5句话即可，**不要写方法论介绍或客套话**）
- 使用表格展示数据对比，标注数据来源
- **报告末尾必须包含两个独立章节：**
  - `## 数据来源说明`：列出本次分析参考/应参考的权威来源清单（从 data-sources 知识库中按相关度筛选），区分「已引用」和「建议参考」
  - `## 合规要求`：列出行业/企业需遵守的现行有效政策法规和标准
- 中文输出
"""
    else:
        system_prompt += f"""

## 分析任务

对「{a}」和「{b}」进行对比分析。

### 重要：请自行判断分析对象的类型组合
- **行业 vs 行业** → 七维度并排对比，每个维度用 `##` 二级标题
- **企业 vs 企业** → 商业模式画布、UE模型、护城河、估值、竞争定位 五大维度 PK，每个维度用 `##` 二级标题
- **企业 vs 行业** 或 **行业 vs 企业** → 先分析企业在该行业中的定位与竞争地位，再展开行业全景分析，最后给出交叉对比结论

### 数据来源规则（极其重要）
**你必须从知识库「data-sources」中列出的权威渠道获取数据：**

1. **官方统计机构**：国家统计局、行业协会、央行、海关总署
2. **公司公开文件**：招股书（最重要！）、年报/季报
3. **券商研究报告**：中金、中信、华泰等
4. **咨询公司报告**：艾瑞、亿欧、麦肯锡、BCG、德勤等
5. **专业数据库**：Wind、Euromonitor、Statista、IT桔子

**引用格式规则：**
- 每条数据后紧跟 `[（来源名称）](URL)`
- **必须优先引用权威源定向检索结果**（国家统计局、巨潮资讯、东方财富研报、行业协会等）
- **禁止使用"未能获取"等消极表述**
- 严禁使用"据XX机构数据"等模糊表述

### 数据时效性要求
- **当前年份是{yr}年**。所有数据必须优先使用{yr}年和{int(yr)-1}年的最新数据
- 如果搜索结果中只有旧数据，请在报告中明确标注

### 📋 合规要求（新增栏目）
- 在报告末尾增加独立的「## 合规要求」章节
- 列出双方各自需遵守的**现行有效的**政策法规和标准
- 每条法规需包含：**名称、发布单位、发布时间/最新修订时间、全文链接（如有）**
- 对比双方合规环境的异同

### 图表要求
- 当有适合可视化的对比数据时，嵌入图表：
```chart
{{"type": "bar", "title": "图表标题", "labels": ["指标1","指标2"], "values": [100,200], "xlabel": "", "ylabel": ""}}
```
- 对比场景优先使用 bar 展示差异
- **图表 JSON 必须严格合法**：所有括号配对、字符串闭合

### 格式要求
- 每个大段落用 ## 二级标题开头，中文输出
- 全文第一个 ## 之前的内容作为概述（3-5句话即可，**不要写方法论介绍或客套话**）
- **报告末尾必须包含两个独立章节：**
  - `## 数据来源说明`：列出本次分析参考/应参考的权威来源清单，区分「已引用」和「建议参考」
  - `## 合规要求`：列出双方各自需遵守的现行有效政策法规
"""

    return system_prompt


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

    # 构建目录：只包含 ## 开头的章节，排除概述前置语
    toc_entries = [(i, sec) for i, sec in enumerate(sections) if sec.strip().startswith("## ")]

    with col_toc:
        st.markdown('<div class="toc-panel">', unsafe_allow_html=True)
        st.markdown('<div class="toc-title">报告目录</div>', unsafe_allow_html=True)

        for ti, (orig_i, sec) in enumerate(toc_entries):
            title_line = sec.strip().split('\n')[0]
            title = title_line.lstrip('#').strip()
            display = title if len(title) <= 24 else title[:22] + "…"
            is_active = (orig_i == st.session_state[toc_key])

            if st.button(display, key=f"toc_{display_title}_{orig_i}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state[toc_key] = orig_i
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
# 核心流程：搜索 → 流式生成报告 → 流式校验 → 展示
# ============================================================

if start_btn and query:
    mode, a, b, display_title = parse_query(query)
    system_prompt = build_prompt(mode, a, b)

    # ---- Step 1: 多维度并行搜索 ----
    with st.status("🔍 正在多维度搜索...", expanded=True) as search_status:
        st.write(f"**搜索对象**：{display_title}")
        dim_list = "市场规模 · 竞争格局 · 商业模式 · 政策监管 · 技术创新 · 投融资 · 风险挑战"
        st.write(f"**覆盖维度**：{dim_list}")

        # 并行：7维度搜索 + 权威源定向搜索
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as pool:
            future_dims = pool.submit(search_by_dimensions, a, True)
            future_auth = pool.submit(search_authoritative, a, True)
            search_a = future_dims.result()
            auth_a = future_auth.result()

        search_b = ""
        auth_b = ""
        if b:
            with ThreadPoolExecutor(max_workers=2) as pool:
                future_dims_b = pool.submit(search_by_dimensions, b, True)
                future_auth_b = pool.submit(search_authoritative, b, True)
                search_b = future_dims_b.result()
                auth_b = future_auth_b.result()

        # 组装搜索结果：通用搜索 + 权威源定向
        search_block = search_a + "\n\n" + auth_a
        if b:
            search_block += "\n\n" + search_b + "\n\n" + auth_b

        result_count = search_block.count("（来源：")
        st.write(f"**获取结果**：约 {result_count} 条（含权威源定向检索）")
        search_status.update(label=f"✅ 搜索完成（7维度 + 权威源定向，约 {result_count} 条结果）", state="complete")

    # ---- Step 2: 流式生成报告 ----
    full_report = ""
    system_prompt += f"\n\n{search_block}\n\n请基于以上搜索结果，结合方法论框架进行分析。优先使用搜索结果中的最新数据。"

    with st.status("✍️ 正在生成报告...", expanded=True) as report_status:
        report_placeholder = st.empty()
        try:
            for chunk in ask_claude_stream(system_prompt, f"请分析：{display_title}"):
                full_report += chunk
                # 只显示最新 2000 字符避免 Streamlit 重绘过重
                preview = full_report if len(full_report) <= 2000 else "…" + full_report[-2000:]
                report_placeholder.markdown(preview + "▌")
        except Exception as e:
            st.error(f"报告生成失败：{e}")
            st.stop()

        report_placeholder.markdown(full_report)
        char_count = len(full_report)
        report_status.update(label=f"✅ 报告生成完成（{char_count:,} 字符）", state="complete")

    # ---- Step 3: 流式事实校验 ----
    checker_prompt = f"""你是一个严格的事实校验员。你的唯一任务是：比对「分析报告」中的事实性声明与「搜索结果」，判断每条声明是否有来源支持。

## 校验规则
1. 从报告中提取所有带有**具体数字（金额、百分比、排名、数量）、具体年份、具体企业名称、具体事件**的声明
2. 在搜索结果中逐一寻找对应的来源——关键数字是否一致、URL 是否可追溯
3. 对每条声明标注状态：
   - ✅ **已验证**：搜索结果中有明确对应数据，且数字吻合
   - ⚠️ **部分匹配**：搜索结果中有相关数据但数字有出入（标注具体差异）
   - ❌ **无来源**：搜索结果中完全未找到对应数据
4. **不要评价报告质量**，不做主观判断，只做事实比对
5. 如果搜索结果不足以验证某条声明，如实标注「无来源」
6. 至少列出报告中最重要的 10-15 条事实性声明

## 输出格式
严格使用 Markdown 表格，不要加额外说明文字：

| # | 声明 | 状态 | 来源 | 备注 |
|---|------|------|------|------|
| 1 | 现制茶饮2026年市场规模5033亿元 | ✅ | [华经产业研究院](https://...) | 数字吻合 |

## 校验对象
{display_title}

## 分析报告
{full_report}

## 搜索结果（事实来源）
{search_block}"""

    full_check = ""
    with st.status("🔎 正在事实校验（逐条比对搜索来源）...", expanded=True) as check_status:
        check_placeholder = st.empty()
        try:
            for chunk in ask_claude_stream(checker_prompt, "请执行事实校验，只输出表格。"):
                full_check += chunk
                check_placeholder.markdown(full_check + "▌")
        except Exception as e:
            full_check = f"*事实校验未能完成：{e}*"

        check_placeholder.markdown(full_check)
        check_status.update(label="✅ 事实校验完成", state="complete")

    # ---- 存储 & 跳转（校验结果插入报告的数据来源说明后） ----
    # 将事实校验结果合并到报告中
    if full_check and "fact_check" not in full_check[:20]:  # 避免重复
        merged_report = re.sub(
            r'(## 数据来源说明.*?)(?=\n## |\Z)',
            r'\1\n\n### 事实校验\n' + full_check,
            full_report,
            count=1,
            flags=re.DOTALL,
        )
        # 如果没匹配到 ## 数据来源说明，追加到末尾
        if merged_report == full_report:
            merged_report = full_report + "\n\n## 数据来源与事实校验\n\n" + full_check
    else:
        merged_report = full_report

    st.session_state["report_response"] = merged_report
    st.session_state["report_title"] = display_title
    st.session_state["report_query"] = query
    st.session_state["search_block"] = search_block

    saved_path = save_report(display_title, merged_report)
    st.toast(f"报告已自动存档", icon="📄")
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
