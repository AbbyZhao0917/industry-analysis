"""
行业研究工作站 —— 首页

基于肖璟《如何快速了解一个行业》方法论
部署端口: 8513
"""

import streamlit as st

st.set_page_config(
    page_title="行业研究工作站",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---- 侧边栏 ----
with st.sidebar:
    st.title("🔍 行业研究工作站")
    st.caption("基于肖璟《如何快速了解一个行业》方法论")
    st.divider()
    st.markdown("""
    **分析模块**
    - 📊 行业分析
    - 🏢 企业分析
    - ⚔️ 企业对比
    - 📈 行业对比
    - 🧰 研究工具箱
    - 📋 报告中心
    """)
    st.divider()
    st.markdown("**知识库**")
    st.markdown("- [产业生命周期](/知识库)")
    st.markdown("- [商业模式画布](/知识库)")
    st.markdown("- [护城河框架](/知识库)")
    st.caption("v0.1.0 · ECS:8513")

# ---- 主页 ----
st.title("🔍 行业研究工作站")
st.markdown(
    "基于 **肖璟《如何快速了解一个行业》**（2025，人民邮电出版社）的完整方法论，"
    "提供行业与企业的系统化分析工具。"
)

# 六模块卡片
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📊 行业分析
    输入行业名称，自动搜索最新数据，按**七维度框架**（可行性/规模性/防守性/
    盈利性/估值/外部因素/景气度）输出完整研究报告。

    → 打开侧边栏进入
    """)

    st.markdown("""
    ### 🏢 企业分析
    输入企业名称，输出**商业模式画布**、**UE单位经济模型**、
    **护城河评分卡**、竞争定位与估值框架。

    → 打开侧边栏进入
    """)

with col2:
    st.markdown("""
    ### ⚔️ 企业对比
    两家企业并排PK：商业模式画布、UE模型关键指标、
    护城河评分、估值对比，输出综合判效。

    → 打开侧边栏进入
    """)

    st.markdown("""
    ### 📈 行业对比
    两个行业七维度并排对比：生命周期定位、可行性、
    规模性、防守性、盈利性、估值、外部因素、景气度。

    → 打开侧边栏进入
    """)

with col3:
    st.markdown("""
    ### 🧰 研究工具箱
    议题树生成（MECE拆解）、数据源推荐引擎、
    AI辅助研究流程向导（资讯料理法三阶段）。

    → 打开侧边栏进入
    """)

    st.markdown("""
    ### 📋 报告中心
    历史分析记录、报告模板管理、
    PDF/Word一键导出。

    → 打开侧边栏进入
    """)

st.divider()

# 方法论概览
st.subheader("分析框架：七大维度")

cols = st.columns(7)
dimensions = [
    ("🔬 可行性", "商业模式\n跑得通吗？"),
    ("📐 规模性", "市场天花板\n有多高？"),
    ("🛡️ 防守性", "护城河\n够深吗？"),
    ("💰 盈利性", "钱被谁\n赚走了？"),
    ("📊 估值", "当前阶段\n值多少钱？"),
    ("🌍 外部因素", "PEST\n驱动力？"),
    ("📡 景气度", "当前行业\n冷热如何？"),
]

for col, (title, desc) in zip(cols, dimensions):
    with col:
        st.markdown(f"**{title}**")
        st.caption(desc)

st.caption("方法来源：肖璟《如何快速了解一个行业》第2-8章 · 产业生命周期主线")