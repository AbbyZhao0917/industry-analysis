"""
资源库 —— 书中推荐的研究数据源 & 分析工具
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
from app.utils.style import inject_css

st.set_page_config(page_title="资源库 · 经纬", page_icon="◈", layout="wide")

inject_css()

st.markdown(
    '<div class="page-title-section">'
    '<h1 style="margin-bottom: 4px;">资源库</h1>'
    '<div class="page-subtitle">'
    '书中推荐的研究数据源 & 分析工具 · 选自肖璟《如何快速了解一个行业》第12章'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 筛选输入 ----
st.markdown('<div class="card">', unsafe_allow_html=True)
keyword = st.text_input(
    "按行业 / 数据类型筛选（可选）",
    placeholder="例如：消费、餐饮、汽车、宏观...",
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)

# ---- 资源数据 ----
# 从 data-sources.md 结构化提取

CATEGORIES = {
    "统计机构": [
        {"name": "国家统计局", "desc": "GDP、CPI、PMI、人口、社零、工业增加值、固定资产投资", "url": "https://www.stats.gov.cn/", "tag": "免费"},
        {"name": "中国人民银行", "desc": "利率、货币供应(M2)、信贷、外汇储备", "url": "https://www.pbc.gov.cn/", "tag": "免费"},
        {"name": "中国海关总署", "desc": "进出口贸易数据", "url": "https://www.customs.gov.cn/", "tag": "免费"},
        {"name": "商务部", "desc": "消费市场、外资、对外投资", "url": "https://www.mofcom.gov.cn/", "tag": "免费"},
        {"name": "工信部", "desc": "工业运行、通信业数据", "url": "https://www.miit.gov.cn/", "tag": "免费"},
        {"name": "IMF 国际货币基金组织", "desc": "全球经济展望、各国宏观数据", "url": "https://www.imf.org/", "tag": "免费"},
        {"name": "World Bank 世界银行", "desc": "全球发展数据", "url": "https://www.worldbank.org/", "tag": "免费"},
        {"name": "WTO 世界贸易组织", "desc": "全球贸易数据", "url": "https://www.wto.org/", "tag": "免费"},
    ],
    "行业协会": [
        {"name": "CCFA 中国连锁经营协会", "desc": "连锁零售/餐饮百强榜单、行业报告", "url": "https://www.ccfa.org.cn/", "tag": "部分免费"},
        {"name": "中国汽车工业协会", "desc": "汽车产销量、新能源车月度数据", "url": "https://www.caam.org.cn/", "tag": "免费"},
        {"name": "中国酒业协会", "desc": "白酒/啤酒产量和销售数据", "url": "https://www.cada.cc/", "tag": "部分免费"},
        {"name": "中国烹饪协会", "desc": "餐饮行业数据", "url": "https://www.ccas.com.cn/", "tag": "部分免费"},
        {"name": "中国半导体行业协会", "desc": "半导体产业数据", "url": "https://www.csia.net.cn/", "tag": "部分免费"},
        {"name": "中国光伏行业协会", "desc": "光伏产业数据", "url": "https://www.chinapv.org.cn/", "tag": "部分免费"},
    ],
    "券商研报渠道": [
        {"name": "东方财富网", "desc": "免费研报，覆盖面广", "url": "https://www.eastmoney.com/", "tag": "免费"},
        {"name": "同花顺", "desc": "免费研报", "url": "https://www.10jqka.com.cn/", "tag": "免费"},
        {"name": "Wind 万得", "desc": "中国最全的金融数据终端", "url": "https://www.wind.com.cn/", "tag": "付费"},
        {"name": "Choice 东方财富终端", "desc": "付费版东方财富，性价比高", "url": "https://choice.eastmoney.com/", "tag": "付费"},
    ],
    "咨询与研究机构": [
        {"name": "艾瑞咨询", "desc": "互联网、新经济领域", "url": "https://www.iresearch.cn/", "tag": "部分免费"},
        {"name": "易观分析", "desc": "数字经济领域", "url": "https://www.analysys.cn/", "tag": "部分免费"},
        {"name": "亿欧智库", "desc": "科技+产业融合研究", "url": "https://www.iyiou.com/", "tag": "部分免费"},
        {"name": "麦肯锡 McKinsey", "desc": "战略、数字化转型", "url": "https://www.mckinsey.com/", "tag": "部分免费"},
        {"name": "BCG 波士顿咨询", "desc": "战略、创新、消费品", "url": "https://www.bcg.com/", "tag": "部分免费"},
        {"name": "德勤 Deloitte", "desc": "各行业研究报告", "url": "https://www.deloitte.com/", "tag": "部分免费"},
    ],
    "专业数据库": [
        {"name": "Bloomberg 彭博", "desc": "全球金融数据终端，覆盖最全", "url": "https://www.bloomberg.com/", "tag": "付费"},
        {"name": "Euromonitor 欧睿", "desc": "消费品市场数据", "url": "https://www.euromonitor.com/", "tag": "付费"},
        {"name": "企查查 / 天眼查", "desc": "企业工商信息、股权结构", "url": "https://www.qcc.com/", "tag": "基础免费"},
        {"name": "IT桔子", "desc": "创投融资数据", "url": "https://www.itjuzi.com/", "tag": "基础免费"},
        {"name": "IDC", "desc": "IT/科技市场数据", "url": "https://www.idc.com/", "tag": "付费"},
        {"name": "Gartner", "desc": "IT技术成熟度、魔力象限", "url": "https://www.gartner.com/", "tag": "付费"},
        {"name": "Statista", "desc": "全球各行业统计数据", "url": "https://www.statista.com/", "tag": "部分免费"},
    ],
    "另类数据来源": [
        {"name": "卫星图像数据", "desc": "工厂开工率、港口吞吐量、农作物种植面积", "url": "—", "tag": "付费"},
        {"name": "招聘数据", "desc": "企业扩张/裁员趋势、新业务方向——各大招聘网站", "url": "—", "tag": "间接获取"},
        {"name": "电商评论", "desc": "产品热度、消费者体验——天猫/京东/拼多多公开评论", "url": "—", "tag": "爬取获取"},
        {"name": "社交媒体情绪", "desc": "品牌口碑、趋势热度——微博/小红书/抖音", "url": "—", "tag": "爬取获取"},
    ],
    "公司公开信息": [
        {"name": "招股说明书", "desc": "最全面的公开信息源——包含行业分析章节、商业模式、财务数据", "url": "上交所/深交所/港交所官网", "tag": "免费"},
        {"name": "年报 / 季报", "desc": "最新财务数据、经营分析", "url": "各交易所 + 巨潮资讯网 cninfo.com.cn", "tag": "免费"},
        {"name": "投资者演示材料", "desc": "业务亮点、战略方向——公司投资者关系网站", "url": "—", "tag": "免费"},
    ],
}

# ---- 筛选逻辑 ----
def matches(resource, kw):
    if not kw:
        return True
    kw_lower = kw.lower()
    return (
        kw_lower in resource["name"].lower()
        or kw_lower in resource["desc"].lower()
        or kw_lower in resource.get("url", "").lower()
    )

def tag_color(tag):
    colors = {
        "免费": ("#ECFDF5", "#065F46"),
        "部分免费": ("#FEF3C7", "#92400E"),
        "付费": ("#F3E8FF", "#6B21A8"),
        "基础免费": ("#ECFDF5", "#065F46"),
        "爬取获取": ("#E0E7FF", "#3730A3"),
        "间接获取": ("#FEF2F2", "#991B1B"),
    }
    return colors.get(tag, ("#F3F4F6", "#374151"))

# ---- 渲染资源卡片 ----
for category, resources in CATEGORIES.items():
    filtered = [r for r in resources if matches(r, keyword)]
    if not filtered:
        continue

    st.markdown(
        f'<div style="font-family: Georgia, serif; font-size: 18px; font-weight: 600; '
        f'color: #2C3338; margin-top: 28px; margin-bottom: 12px;">{category}</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, res in enumerate(filtered):
        bg, fg = tag_color(res["tag"])
        url_display = res["url"] if res["url"] != "—" else ""
        url_html = (
            f'<a href="{res["url"]}" target="_blank" '
            f'style="color: #2D5A4B; font-size: 13px; text-decoration: none;">{res["url"]}</a>'
            if res["url"] != "—" else
            f'<span style="color: #9CA3AF; font-size: 13px;">{res["url"]}</span>'
        )

        with cols[i % 2]:
            st.markdown(f"""
            <div class="module-card" style="padding: 16px 20px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="font-size: 16px; font-weight: 600; color: #2C3338;">{res["name"]}</div>
                    <span style="font-size: 11px; background: {bg}; color: {fg};
                    padding: 2px 8px; border-radius: 4px; white-space: nowrap; margin-left: 8px;">{res["tag"]}</span>
                </div>
                <div style="font-size: 13px; color: #6B7280; margin-top: 6px; line-height: 1.5;">{res["desc"]}</div>
                <div style="margin-top: 8px;">{url_html}</div>
            </div>
            """, unsafe_allow_html=True)

# ---- 底部：搜索技巧 ----
st.markdown("""
<div class="framework-section" style="margin-top: 32px;">
    <div class="framework-title">信息检索技巧</div>
    <table style="width: 100%; font-size: 14px; border-collapse: collapse;">
        <tr>
            <td style="padding: 6px 0; font-weight: 600; width: 35%;">限定来源搜索</td>
            <td style="padding: 6px 0; color: #6B7280;"><code style="font-size: 13px;">关键词 site:stats.gov.cn</code></td>
        </tr>
        <tr>
            <td style="padding: 6px 0; font-weight: 600;">搜索 PDF 研报</td>
            <td style="padding: 6px 0; color: #6B7280;"><code style="font-size: 13px;">行业名 filetype:pdf</code></td>
        </tr>
        <tr>
            <td style="padding: 6px 0; font-weight: 600;">公众号搜索</td>
            <td style="padding: 6px 0; color: #6B7280;">微信搜一搜找行业 KOL 分析文章</td>
        </tr>
        <tr>
            <td style="padding: 6px 0; font-weight: 600;">研报标题模式</td>
            <td style="padding: 6px 0; color: #6B7280;">搜索："行业名 深度报告" 或 "行业名 年度策略"</td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div style="font-size: 13px; color: #9CA3AF; margin-top: 24px;">'
    '数据来源：肖璟《如何快速了解一个行业》(2025) 第12章 · 各机构官网'
    '</div>',
    unsafe_allow_html=True,
)
