"""
经纬 · 行业洞察平台 —— 首页

基于肖璟《如何快速了解一个行业》(2025，人民邮电出版社) 方法论
"""
import streamlit as st
from utils.style import inject_css

st.set_page_config(
    page_title="经纬 · 行业洞察",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ---- 侧边栏 ----
with st.sidebar:
    st.markdown(
        '<div style="font-family: Georgia, serif; font-size: 22px; font-weight: 600; '
        'color: #2C3338; margin-bottom: 4px;">经纬</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size: 13px; color: #6B7280; margin-bottom: 16px;">行业洞察平台</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div style="font-size: 12px; color: #9CA3AF; margin-top: 8px;">'
        '方法论来源：肖璟《如何快速了解一个行业》<br>'
        '2025，人民邮电出版社</div>',
        unsafe_allow_html=True,
    )

# ---- 主页 Hero ----
st.markdown(
    '<div class="hero-title">经纬 · 行业洞察</div>'
    '<div class="hero-subtitle">'
    '基于产业生命周期主线的七维度分析框架<br>'
    '输入行业或企业名称，自动检索最新公开数据，输出结构化研究报告'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 六模块卡片 ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="module-card">
        <div class="module-card-title">行业分析</div>
        <div class="module-card-desc">
            输入行业名称，自动检索最新公开数据，按七维度框架（可行性 · 规模性 · 防守性 · 盈利性 · 估值 · 外部因素 · 景气度）输出完整研究报告。
        </div>
        <a class="module-card-link" href="/行业分析">进入模块</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <div class="module-card-title">行业对比</div>
        <div class="module-card-desc">
            两个行业七维度并排对比：生命周期定位、可行性、规模性、防守性、盈利性、估值、外部因素、景气度。差异高亮，选择建议。
        </div>
        <a class="module-card-link" href="/行业对比">进入模块</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="module-card">
        <div class="module-card-title">企业分析</div>
        <div class="module-card-desc">
            输入企业名称，输出商业模式画布、UE 单位经济模型、护城河评分卡、竞争定位与估值框架。对照行业基准标注。
        </div>
        <a class="module-card-link" href="/企业分析">进入模块</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <div class="module-card-title">研究工具箱</div>
        <div class="module-card-desc">
            假设驱动的议题树生成（MECE 拆解）、数据源推荐引擎、AI 辅助研究流程向导（资讯料理法：备菜 · 烹饪 · 摆盘）。
        </div>
        <a class="module-card-link" href="/研究工具箱">进入模块</a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="module-card">
        <div class="module-card-title">企业对比</div>
        <div class="module-card-desc">
            两家企业并排 PK：商业模式画布、UE 指标、护城河评分、估值框架、竞争定位。综合判效与选择建议。
        </div>
        <a class="module-card-link" href="/企业对比">进入模块</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="module-card">
        <div class="module-card-title">报告中心</div>
        <div class="module-card-desc">
            历史分析记录归档、报告模板管理。支持导出 Markdown / Word / PDF 格式。
        </div>
        <a class="module-card-link" href="/报告中心">进入模块</a>
    </div>
    """, unsafe_allow_html=True)

# ---- 七维度框架概览 ----
st.markdown("""
<div class="framework-section">
    <div class="framework-title">分析框架：七大维度</div>
""", unsafe_allow_html=True)

cols = st.columns(7)
dimensions = [
    ("可行性", "商业模式能否跑通"),
    ("规模性", "市场天花板有多高"),
    ("防守性", "护城河够不够深"),
    ("盈利性", "钱被谁赚走了"),
    ("估值", "当前阶段值多少钱"),
    ("外部因素", "PEST 驱动力"),
    ("景气度", "行业当前冷热"),
]

for col, (label, desc) in zip(cols, dimensions):
    with col:
        st.markdown(
            f'<div class="dim-label">{label}</div>'
            f'<div class="dim-desc">{desc}</div>',
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<div class="methodology-note">'
    '方法论来源：肖璟《如何快速了解一个行业》(2025，人民邮电出版社) · 产业生命周期主线'
    '</div>',
    unsafe_allow_html=True,
)

# JS: 侧边栏 "main" → "首页"
st.markdown("""
<script>
(function() {
    const nav = document.querySelector('[data-testid=\"stSidebarNav\"]');
    if (!nav) return;
    const links = nav.querySelectorAll('a');
    links.forEach(function(a) {
        const span = a.querySelector('span');
        if (span && span.textContent.trim() === 'main') {
            span.textContent = '首页';
        }
    });
})();
</script>
""", unsafe_allow_html=True)
