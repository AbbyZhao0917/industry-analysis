"""
资源库 —— 《如何快速了解一个行业》全书资源清单
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
    '《如何快速了解一个行业》全书资源清单 · 按类别整理 · 点击名称直达'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---- 搜索筛选 ----
st.markdown('<div class="card">', unsafe_allow_html=True)
keyword = st.text_input(
    "按名称 / 描述 / 类别筛选",
    placeholder="例如：消费、餐饮、汽车、宏观、金融...",
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# 全书资源（来自 Word 文档 + data-sources.md，去重后按类别整理）
# ============================================================

CATEGORIES = {
    "金融数据库": [
        {"name": "Choice 金融终端", "desc": "东方财富旗下，适合普通投资者，价格相对便宜", "url": "https://choice.eastmoney.com/", "tag": "付费"},
        {"name": "iFinD 同花顺", "desc": "同花顺旗下，普通投资者够用，价格相对便宜", "url": "https://www.51ifind.com/", "tag": "付费"},
        {"name": "Wind 万得", "desc": "中国最全的金融数据终端", "url": "https://www.wind.com.cn/", "tag": "付费"},
        {"name": "CEIC 香港环亚经济数据", "desc": "全面的宏观经济数据，受经济学家青睐", "url": "https://www.ceicdata.com/", "tag": "付费"},
        {"name": "慧博投研", "desc": "国内较早的研报下载平台，已转型做数据终端", "url": "https://www.hibor.com.cn/", "tag": "部分免费"},
        {"name": "萝卜投研", "desc": "通联数据旗下，海量行业数据库，搜研报图表方便，每日有免费额度", "url": "https://robo.datayes.com/", "tag": "部分免费"},
        {"name": "彭博 Bloomberg", "desc": "海外知名数据终端，价格昂贵，需配备专用硬件", "url": "https://www.bloomberg.com/", "tag": "付费"},
        {"name": "Capital IQ", "desc": "标普全球旗下，涵盖全球上市公司/非上市公司/资管机构数据", "url": "https://www.capitaliq.com/", "tag": "付费"},
        {"name": "Factiva", "desc": "道琼斯旗下商业新闻与市场情报数据库", "url": "https://www.dowjones.com/professional/factiva/", "tag": "付费"},
        {"name": "企查查 / 天眼查", "desc": "企业工商信息、知识产权、司法风险查询", "url": "https://www.qcc.com/", "tag": "基础免费"},
        {"name": "IT桔子 / 36氪创投平台", "desc": "企业融资信息查询", "url": "https://www.itjuzi.com/", "tag": "基础免费"},
    ],
    "学术数据库": [
        {"name": "谷歌学术", "desc": "全球最大的学术搜索引擎", "url": "https://scholar.google.com/", "tag": "免费"},
        {"name": "知网 CNKI", "desc": "中国最大的中文学术文献数据库", "url": "https://www.cnki.net/", "tag": "付费"},
        {"name": "维普", "desc": "中文科技期刊数据库", "url": "https://www.cqvip.com/", "tag": "付费"},
        {"name": "万方", "desc": "中文学术数据库", "url": "https://www.wanfangdata.com.cn/", "tag": "付费"},
        {"name": "掌桥", "desc": "一站式科研服务平台", "url": "https://www.zhangqiaokeyan.com/", "tag": "部分免费"},
        {"name": "JSTOR", "desc": "过期学术期刊全文数据库", "url": "https://www.jstor.org/", "tag": "部分免费"},
        {"name": "ResearchGate", "desc": "学术社交网络，研究人员分享论文", "url": "https://www.researchgate.net/", "tag": "免费"},
        {"name": "Elsevier", "desc": "全球最大的科学文献出版商之一", "url": "https://www.elsevier.com/", "tag": "付费"},
        {"name": "百度学术", "desc": "中文文献搜索，可直接搜索学术论文", "url": "https://xueshu.baidu.com/", "tag": "免费"},
    ],
    "官方机构（国内）": [
        {"name": "国家发展和改革委员会", "desc": "分省份/地区经济数据、煤电油气、物流仓储、重要商品价格、粮食收购进度", "url": "https://www.ndrc.gov.cn/", "tag": "免费"},
        {"name": "教育部", "desc": "学校/教师/学生数量、专业招生情况等教育数据", "url": "https://www.moe.gov.cn/", "tag": "免费"},
        {"name": "工业和信息化部", "desc": "原材料/装备/消费品工业、通信业、电子信息、软件业、互联网、网络安全", "url": "https://www.miit.gov.cn/", "tag": "免费"},
        {"name": "财政部", "desc": "财政收支、税收、土地出让金、央国企运营、彩票销售等", "url": "https://www.mof.gov.cn/", "tag": "免费"},
        {"name": "人力资源和社会保障部", "desc": "就业数据、社保数据", "url": "https://www.mohrss.gov.cn/", "tag": "免费"},
        {"name": "自然资源部", "desc": "土地/矿产/海洋/测绘/地质数据", "url": "https://www.mnr.gov.cn/", "tag": "免费"},
        {"name": "生态环境部", "desc": "生态环境统计年报", "url": "https://www.mee.gov.cn/", "tag": "免费"},
        {"name": "住房和城乡建设部", "desc": "城乡建设统计年鉴、建筑业数据", "url": "https://www.mohurd.gov.cn/", "tag": "免费"},
        {"name": "交通运输部", "desc": "水运/公路/铁路/民航/邮政/城市客运/港口/运价指数", "url": "https://www.mot.gov.cn/", "tag": "免费"},
        {"name": "农业农村部", "desc": "农产品价格、农产品进出口数据", "url": "https://www.moa.gov.cn/", "tag": "免费"},
        {"name": "商务部", "desc": "国际投资/国际业务/国际贸易数据、消费市场、外资、对外投资", "url": "https://www.mofcom.gov.cn/", "tag": "免费"},
        {"name": "国家卫生健康委员会", "desc": "国家基本药物目录、医卫机构名单", "url": "https://www.nhc.gov.cn/", "tag": "免费"},
        {"name": "国家金融监督管理总局", "desc": "银行业、保险业数据", "url": "https://www.nfra.gov.cn/", "tag": "免费"},
        {"name": "中国证监会", "desc": "证券市场/期货市场数据、合法机构名录", "url": "https://www.csrc.gov.cn/", "tag": "免费"},
        {"name": "国家体育总局", "desc": "国民体质监测数据", "url": "https://www.sport.gov.cn/", "tag": "免费"},
        {"name": "国家统计局", "desc": "GDP/CPI/PMI/人口/社零/工业增加值/固定资产投资等各类宏观数据", "url": "https://www.stats.gov.cn/", "tag": "免费"},
        {"name": "国家医疗保障局", "desc": "医疗保险和生育保险数据", "url": "https://www.nhsa.gov.cn/", "tag": "免费"},
        {"name": "中国人民银行", "desc": "社会融资规模、货币供给(M2)、金融市场统计、银行家/企业家调查问卷、货币政策", "url": "https://www.pbc.gov.cn/", "tag": "免费"},
        {"name": "国家外汇管理局", "desc": "国际收支平衡表、结售汇数据、官方储备资产数据", "url": "https://www.safe.gov.cn/", "tag": "免费"},
        {"name": "国家铁路局", "desc": "铁路发送量数据", "url": "https://www.nra.gov.cn/", "tag": "免费"},
        {"name": "中国民用航空局", "desc": "民航主要生产指标统计数据", "url": "https://www.caac.gov.cn/", "tag": "免费"},
        {"name": "国家邮政局", "desc": "邮政行业运行数据", "url": "https://www.spb.gov.cn/", "tag": "免费"},
        {"name": "中国海关总署", "desc": "进出口贸易数据", "url": "https://www.customs.gov.cn/", "tag": "免费"},
    ],
    "协会/交易机构": [
        {"name": "中国外汇交易中心", "desc": "货币市场报价利率、债券/外汇市场价格", "url": "https://www.chinamoney.com.cn/", "tag": "免费"},
        {"name": "中国证券投资基金业协会", "desc": "基金资产管理规模、规模排名、类型分布", "url": "https://www.amac.org.cn/", "tag": "免费"},
        {"name": "中国债券信息网", "desc": "债券收益率、债券指数等债券数据", "url": "https://www.chinabond.com.cn/", "tag": "免费"},
        {"name": "中国互联网络信息中心", "desc": "中国互联网络发展状况统计数据", "url": "https://www.cnnic.net.cn/", "tag": "免费"},
        {"name": "上海证券交易所", "desc": "证券市场数据、公司披露数据", "url": "https://www.sse.com.cn/", "tag": "免费"},
        {"name": "深圳证券交易所", "desc": "证券市场数据、公司披露数据", "url": "https://www.szse.cn/", "tag": "免费"},
        {"name": "CCFA 中国连锁经营协会", "desc": "连锁零售/餐饮百强榜单、行业报告", "url": "https://www.ccfa.org.cn/", "tag": "部分免费"},
        {"name": "中国汽车工业协会", "desc": "汽车产销量、新能源车月度数据", "url": "https://www.caam.org.cn/", "tag": "免费"},
        {"name": "乘用车市场信息联席分会", "desc": "乘用车市场产销数据、周度/月度零售数据", "url": "https://www.cpcaauto.com/", "tag": "免费"},
        {"name": "中国酒业协会", "desc": "白酒/啤酒产量和销售数据", "url": "https://www.cada.cc/", "tag": "部分免费"},
        {"name": "中国烹饪协会", "desc": "餐饮行业数据", "url": "https://www.ccas.com.cn/", "tag": "部分免费"},
        {"name": "中国半导体行业协会", "desc": "半导体产业数据", "url": "https://www.csia.net.cn/", "tag": "部分免费"},
        {"name": "中国光伏行业协会", "desc": "光伏产业数据", "url": "https://www.chinapv.org.cn/", "tag": "部分免费"},
    ],
    "国际机构": [
        {"name": "世界银行 World Bank", "desc": "全球发展数据", "url": "https://www.worldbank.org/", "tag": "免费"},
        {"name": "国际货币基金组织 IMF", "desc": "全球经济展望、各国宏观数据", "url": "https://www.imf.org/", "tag": "免费"},
        {"name": "经济合作与发展组织 OECD", "desc": "各类宏观数据", "url": "https://www.oecd.org/", "tag": "免费"},
        {"name": "国际清算银行 BIS", "desc": "经济数据", "url": "https://www.bis.org/", "tag": "免费"},
        {"name": "国际能源署 IEA", "desc": "能源供需/进出口/价格/排放数据", "url": "https://www.iea.org/", "tag": "免费"},
        {"name": "联合国粮农组织 FAO", "desc": "245+国家和地区的粮食与农业数据（农作物/畜牧业/林业等）", "url": "https://www.fao.org/", "tag": "免费"},
        {"name": "WTO 世界贸易组织", "desc": "全球贸易数据", "url": "https://www.wto.org/", "tag": "免费"},
    ],
    "调研机构": [
        {"name": "艾瑞咨询", "desc": "中国新经济与产业数字化洞察，累计3000+行业研究报告", "url": "https://www.iresearch.cn/", "tag": "部分免费"},
        {"name": "艾媒集团 iiMedia", "desc": "全球新经济产业第三方数据挖掘和分析机构", "url": "https://www.iimedia.cn/", "tag": "部分免费"},
        {"name": "克而瑞 CRIC", "desc": "不动产垂直领域数字化平台，月度房地产销售/房价成交指数", "url": "https://www.cricchina.com/", "tag": "部分免费"},
        {"name": "七麦数据", "desc": "移动应用数据分析平台，App排名/竞品对比/下载收入预估", "url": "https://www.qimai.cn/", "tag": "部分免费"},
        {"name": "窄门餐眼", "desc": "餐饮数据查询平台（微信小程序），覆盖3万+餐饮品牌", "url": "微信小程序搜索「窄门餐眼」", "tag": "免费"},
        {"name": "今日酒价", "desc": "国内酒类报价等酒业数据（微信公众号）", "url": "微信公众号搜索「今日酒价」", "tag": "免费"},
        {"name": "猫眼专业版", "desc": "电影票房/电视剧热度/电视收视率数据（App）", "url": "App Store/应用商店下载", "tag": "免费"},
        {"name": "奥维云网 AVC", "desc": "智慧家庭领域大数据，家电销售数据", "url": "https://www.avc-mr.com/", "tag": "部分免费"},
        {"name": "上海有色网 SMM", "desc": "有色金属行业综合服务门户，有色/采矿行业数据", "url": "https://www.smm.cn/", "tag": "部分免费"},
        {"name": "益普索 Ipsos", "desc": "全球市场研究集团，消费者洞察/广告研究/媒介研究，可委托调研", "url": "https://www.ipsos.com/", "tag": "付费"},
        {"name": "欧睿 Euromonitor", "desc": "全球知名市场资讯供应商，消费品市场调研数据", "url": "https://www.euromonitor.com/", "tag": "付费"},
        {"name": "埃信华迈 IHS Markit", "desc": "以编制各国PMI闻名（已并入标普全球），财新PMI由其联合编制", "url": "https://www.spglobal.com/", "tag": "付费"},
        {"name": "睿勤 Preqin", "desc": "另类资产行业数据/市场分析，PE/VC/对冲基金数据", "url": "https://www.preqin.com/", "tag": "付费"},
        {"name": "易观分析", "desc": "数字经济领域", "url": "https://www.analysys.cn/", "tag": "部分免费"},
        {"name": "亿欧智库", "desc": "科技+产业融合研究", "url": "https://www.iyiou.com/", "tag": "部分免费"},
        {"name": "IDC", "desc": "IT/科技市场数据", "url": "https://www.idc.com/", "tag": "付费"},
        {"name": "Gartner", "desc": "IT技术成熟度/魔力象限", "url": "https://www.gartner.com/", "tag": "付费"},
        {"name": "Statista", "desc": "全球各行业统计数据", "url": "https://www.statista.com/", "tag": "部分免费"},
    ],
    "搜索引擎": [
        {"name": "i问财", "desc": "智能金融垂直搜索引擎，支持条件搜索（如「连续三年累计分红低于年均利润30%」直接出股票列表）", "url": "https://www.iwencai.com/", "tag": "免费"},
        {"name": "Perplexity", "desc": "AI驱动搜索引擎，爬取网页并用大模型总结相关内容", "url": "https://www.perplexity.ai/", "tag": "免费"},
        {"name": "Wolfram|Alpha", "desc": "老牌语义搜索引擎，GDP等数据自动生成多维度图表，不支持中文", "url": "https://www.wolframalpha.com/", "tag": "免费"},
        {"name": "秘塔AI搜索", "desc": "国内类似Perplexity的AI搜索引擎", "url": "https://metaso.cn/", "tag": "免费"},
    ],
    "百科工具": [
        {"name": "维基百科", "desc": "多语言网络百科全书", "url": "https://www.wikipedia.org/", "tag": "免费"},
        {"name": "MBA智库百科", "desc": "商业类垂直百科，专注经管领域——商业/金融/经济/投资", "url": "https://wiki.mbalib.com/", "tag": "免费"},
        {"name": "Investopedia", "desc": "全球知名投资百科全书，金融术语词典，近年转向交易+课程平台", "url": "https://www.investopedia.com/", "tag": "免费"},
    ],
    "社交媒体与社区": [
        {"name": "经管之家", "desc": "原人大经济论坛，大学生搜寻资料和数据的主要社区", "url": "https://www.jg.com.cn/", "tag": "免费"},
        {"name": "丁香园论坛", "desc": "医疗行业社区，医学/药学/生命科学学术交流", "url": "https://www.dxy.cn/", "tag": "免费"},
        {"name": "雪球", "desc": "投资者社区，个股深度分析讨论", "url": "https://xueqiu.com/", "tag": "免费"},
        {"name": "技术社区", "desc": "GitHub / CSDN / StackOverflow / V2EX / 稀土掘金——程序员/工程师交流分享", "url": "https://github.com/", "tag": "免费"},
        {"name": "量化社区", "desc": "聚宽 / 掘金量化 / BigQuant——量化投资数据/投研工具/学习资源", "url": "https://www.joinquant.com/", "tag": "部分免费"},
        {"name": "券商研究报告渠道", "desc": "东方财富网 eastmoney.com / 同花顺 10jqka.com.cn——免费研报下载", "url": "https://www.eastmoney.com/", "tag": "免费"},
    ],
    "官方研究部门": [
        {"name": "中国人民银行（研究局）", "desc": "发布《中国金融稳定报告》《中国货币政策执行报告》", "url": "https://www.pbc.gov.cn/", "tag": "免费"},
        {"name": "商务部（研究院）", "desc": "发布《中国对外投资合作发展报告》《中国电子商务报告》《中国服务贸易发展报告》", "url": "https://www.mofcom.gov.cn/", "tag": "免费"},
        {"name": "美联储 Federal Reserve", "desc": "发布《褐皮书》(Beige Book)《货币政策报告》等", "url": "https://www.federalreserve.gov/", "tag": "免费"},
    ],
    "学术研究机构": [
        {"name": "财经大学研究", "desc": "不定期发布《中国家庭金融调查报告》等", "url": "需搜索具体报告名称", "tag": "免费"},
        {"name": "密歇根大学", "desc": "定期发布《密歇根消费者信心指数报告》", "url": "https://data.sca.isr.umich.edu/", "tag": "免费"},
        {"name": "斯坦福大学 HAI", "desc": "发布《人工智能指数报告》等", "url": "https://aiindex.stanford.edu/", "tag": "免费"},
        {"name": "NBER 美国国家经济研究局", "desc": "发表高水平工作论文（Working Papers）", "url": "https://www.nber.org/", "tag": "免费"},
    ],
    "咨询公司": [
        {"name": "麦肯锡 McKinsey", "desc": "战略、数字化转型领域", "url": "https://www.mckinsey.com/", "tag": "部分免费"},
        {"name": "波士顿咨询 BCG", "desc": "战略、创新领域", "url": "https://www.bcg.com/", "tag": "部分免费"},
        {"name": "贝恩 Bain", "desc": "消费品、私募领域", "url": "https://www.bain.com/", "tag": "部分免费"},
        {"name": "罗兰贝格 Roland Berger", "desc": "欧洲领先战略咨询公司，汽车/工业品领域强", "url": "https://www.rolandberger.com/", "tag": "部分免费"},
        {"name": "德勤 Deloitte", "desc": "各行业研究报告", "url": "https://www.deloitte.com/", "tag": "部分免费"},
    ],
    "公司公开信息": [
        {"name": "招股说明书", "desc": "最全面的公开信息源——行业分析章节（第三方咨询公司撰写）、商业模式、财务数据", "url": "上交所/深交所/港交所/纽交所官网 + 巨潮资讯网 cninfo.com.cn", "tag": "免费"},
        {"name": "年报 / 季报", "desc": "最新财务数据、经营分析", "url": "https://www.cninfo.com.cn/", "tag": "免费"},
        {"name": "投资者演示材料", "desc": "业务亮点、战略方向——各公司投资者关系网站", "url": "各公司官网-投资者关系页", "tag": "免费"},
    ],
}

# ---- 渲染 ----
def tag_style(tag):
    colors = {
        "免费": ("#ECFDF5", "#065F46"),
        "部分免费": ("#FEF3C7", "#92400E"),
        "付费": ("#F3E8FF", "#6B21A8"),
        "基础免费": ("#ECFDF5", "#065F46"),
    }
    return colors.get(tag, ("#F3F4F6", "#374151"))

for category, resources in CATEGORIES.items():
    # 筛选
    if keyword:
        kw = keyword.lower()
        filtered = [r for r in resources if kw in r["name"].lower() or kw in r["desc"].lower() or kw in category.lower()]
    else:
        filtered = resources

    if not filtered:
        continue

    # 类别标题
    st.markdown(
        f'<div style="font-family: Georgia, serif; font-size: 18px; font-weight: 600; '
        f'color: #2C3338; margin-top: 28px; margin-bottom: 12px;">'
        f'{category} <span style="font-size:13px; color:#9CA3AF; font-weight:400;">({len(filtered)}个)</span></div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, res in enumerate(filtered):
        bg, fg = tag_style(res["tag"])
        # 构建链接
        if res["url"].startswith("http"):
            link = f'<a href="{res["url"]}" target="_blank" style="color: #2D5A4B; font-size: 13px; text-decoration: none;">{res["url"]}</a>'
        else:
            link = f'<span style="color: #9CA3AF; font-size: 13px;">{res["url"]}</span>'

        with cols[i % 2]:
            st.markdown(f"""
            <div class="module-card" style="padding: 14px 18px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
                    <a href="{res['url']}" target="_blank" style="font-size: 15px; font-weight: 600; color: #1D4ED8; text-decoration: none; line-height: 1.3;">
                        {res["name"]}
                    </a>
                    <span style="font-size: 10px; background: {bg}; color: {fg};
                    padding: 1px 6px; border-radius: 3px; white-space: nowrap; flex-shrink: 0;">{res["tag"]}</span>
                </div>
                <div style="font-size: 13px; color: #6B7280; margin-top: 4px; line-height: 1.5;">{res["desc"]}</div>
                <div style="margin-top: 6px;">{link}</div>
            </div>
            """, unsafe_allow_html=True)

# ---- 底部 ----
st.markdown(
    '<div style="font-size: 13px; color: #9CA3AF; margin-top: 32px; text-align: center;">'
    '数据来源：肖璟《如何快速了解一个行业》(2025，人民邮电出版社) 全书资源清单 · 各机构官网'
    '</div>',
    unsafe_allow_html=True,
)
