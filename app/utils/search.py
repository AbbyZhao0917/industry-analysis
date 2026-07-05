"""联网搜索 —— Tavily（搜索）+ Firecrawl（深度抓取）双引擎"""
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from dotenv import load_dotenv
from tavily import TavilyClient
from firecrawl import FirecrawlApp

load_dotenv()

FIRECRAWL_KEY = os.getenv("FIRECRAWL_API_KEY", "")


def _get_tavily() -> TavilyClient:
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        raise RuntimeError("未设置 TAVILY_API_KEY")
    return TavilyClient(api_key=key)


def _get_firecrawl() -> FirecrawlApp:
    if not FIRECRAWL_KEY:
        return None
    return FirecrawlApp(api_key=FIRECRAWL_KEY)


def search_web(query: str, max_results: int = 5) -> str:
    """Tavily 快速搜索，返回摘要 + URL"""
    yr = str(datetime.now().year)
    try:
        client = _get_tavily()
        response = client.search(query, max_results=max_results, search_depth="basic")
        results = response.get("results", [])
    except Exception as e:
        return f"（搜索服务不可用：{e}，以下数据来自模型训练知识。建议自行核验{yr}年最新数据。）"

    if not results:
        return f"（搜索无结果，以下数据来自模型训练知识。建议自行核验{yr}年最新数据。）"

    lines = []
    for i, r in enumerate(results, 1):
        url_str = f"（来源：{r.get('url', '')}）" if r.get("url") else ""
        lines.append(f"{i}. **{r.get('title', '')}**\n   {r.get('content', '')[:300]} {url_str}")
    return "\n\n".join(lines)


def scrape_url(url: str) -> str:
    """Firecrawl 抓取单页全文（markdown 格式）"""
    fc = _get_firecrawl()
    if not fc:
        return ""

    try:
        result = fc.scrape_url(url, formats=["markdown"])
        md = result.markdown if hasattr(result, "markdown") else ""
        return md[:4000] if md else ""
    except Exception:
        return ""


def search_web_deep(query: str, max_results: int = 5, scrape_top: int = 2) -> str:
    """
    深度搜索：Tavily 搜 → Firecrawl 抓取前 N 篇全文 → 合并输出。
    用于需要详细数据的行业/企业分析场景。
    """
    yr = str(datetime.now().year)

    # Step 1: 搜索
    try:
        client = _get_tavily()
        response = client.search(query, max_results=max_results, search_depth="basic")
        results = response.get("results", [])
    except Exception as e:
        return f"（搜索服务不可用：{e}，以下数据来自模型训练知识。建议自行核验{yr}年最新数据。）"

    if not results:
        return f"（搜索无结果，以下数据来自模型训练知识。建议自行核验{yr}年最新数据。）"

    # Step 2: 摘要列表
    lines = ["## 搜索结果摘要"]
    urls_to_scrape = []
    for i, r in enumerate(results, 1):
        url = r.get("url", "")
        lines.append(f"{i}. **{r.get('title', '')}**\n   {r.get('content', '')[:200]}（来源：{url}）")
        if i <= scrape_top and url:
            urls_to_scrape.append(url)

    # Step 3: 深度抓取前 scrape_top 篇
    fc = _get_firecrawl()
    if fc and urls_to_scrape:
        for j, url in enumerate(urls_to_scrape):
            try:
                result = fc.scrape_url(url, formats=["markdown"])
                md = result.markdown if hasattr(result, "markdown") else ""
                if md:
                    lines.append(f"\n## 全文抓取 #{j+1}: {url}\n{md[:3000]}")
            except Exception:
                pass

    return "\n\n".join(lines)


# ---------- 维度定义 ----------

# 行业分析维度 → 搜索 query
_INDUSTRY_DIMENSIONS = [
    ("市场规模与增长", "市场规模 增长率 预测"),
    ("竞争格局",        "竞争格局 头部企业 市场份额 CR5"),
    ("商业模式与盈利",  "商业模式 毛利率 净利率 盈利水平"),
    ("政策与监管",      "政策 监管 法规 准入"),
    ("技术与创新",      "技术 创新 研发 专利 趋势"),
    ("投融资与估值",    "融资 估值 投资 并购"),
    ("风险与挑战",      "风险 挑战 瓶颈 趋势"),
]

# 企业分析维度 → 搜索 query
_COMPANY_DIMENSIONS = [
    ("营收与财报",      "财报 营收 利润 增长率"),
    ("商业模式",        "商业模式 收入结构 盈利模式"),
    ("竞争与护城河",    "竞争优势 护城河 壁垒 差异化"),
    ("UE与成本结构",    "单店模型 客单价 成本结构 UE"),
    ("估值与融资",      "估值 市值 PE PS 融资"),
    ("战略与动态",      "战略 新品 扩张 动态"),
    ("风险与舆情",      "风险 诉讼 舆情 争议"),
]


def _build_dimension_queries(entity_name: str, dimensions: list) -> list:
    """将维度定义转为完整的搜索 query 列表"""
    yr = str(datetime.now().year)
    return [
        (dim_name, f"{entity_name} {query_template} {yr}")
        for dim_name, query_template in dimensions
    ]


def search_by_dimensions(
    entity_name: str,
    is_industry: bool = True,
    max_results: int = 3,
) -> str:
    """
    多维度并行搜索 —— 7 个维度同时搜，合并输出。

    参数：
        entity_name: 行业或企业名称
        is_industry: True=行业维度, False=企业维度
        max_results: 每个维度返回的结果数
    """
    dims = _INDUSTRY_DIMENSIONS if is_industry else _COMPANY_DIMENSIONS
    queries = _build_dimension_queries(entity_name, dims)

    # 并行搜索
    results = {}
    with ThreadPoolExecutor(max_workers=len(queries)) as executor:
        futures = {
            executor.submit(search_web, query, max_results): dim_name
            for dim_name, query in queries
        }
        for future in as_completed(futures):
            dim_name = futures[future]
            try:
                results[dim_name] = future.result()
            except Exception:
                results[dim_name] = "（搜索失败）"

    # 按原始顺序输出
    lines = [f"## 多维度联网搜索结果：{entity_name}"]
    for dim_name, _ in dims:
        content = results.get(dim_name, "（搜索失败）")
        lines.append(f"\n### {dim_name}\n{content}")

    return "\n\n".join(lines)


def search_for_industry(industry_name: str) -> str:
    """快捷入口：行业深度搜索（7维度并行）"""
    return search_by_dimensions(industry_name, is_industry=True)


def search_for_company(company_name: str) -> str:
    """快捷入口：企业深度搜索（7维度并行）"""
    return search_by_dimensions(company_name, is_industry=False)


def search_authoritative(entity_name: str, is_industry: bool = True) -> str:
    """
    定向搜索权威来源 —— 针对国家统计局、行业协会、招股书、券商研报等，
    使用 site: 语法精准搜索，并用 Firecrawl 抓取全文。
    用于填补通用搜索未覆盖的权威数据缺口。
    """
    yr = str(datetime.now().year)

    # 权威源查询列表
    targets = [
        ("国家统计局", f"{entity_name} site:stats.gov.cn"),
        ("商务部/发改委", f"{entity_name} site:mofcom.gov.cn OR site:ndrc.gov.cn"),
        ("艾瑞/亿欧 行业报告", f"{entity_name} 行业报告 site:iresearch.cn OR site:iyiou.com"),
        ("券商研报(东方财富)", f"{entity_name} 深度报告 {yr} site:eastmoney.com"),
        ("巨潮资讯(招股书/年报)", f"{entity_name} 招股说明书 OR 年报 site:cninfo.com.cn"),
    ]

    if is_industry:
        targets.append(("行业协会(CCFA/中烹协等)", f"{entity_name} 行业数据 OR 百强 OR 报告 site:ccfa.org.cn OR site:ccas.com.cn"))
    else:
        targets.append(("企查查/IT桔子(工商/融资)", f"{entity_name} 融资 OR 股东 OR 估值"))
        targets.append(("招股书", f"{entity_name} 招股说明书 filetype:pdf"))

    # 并行搜索
    results = {}
    with ThreadPoolExecutor(max_workers=len(targets)) as executor:
        futures = {
            executor.submit(search_web, query, max_results=2): label
            for label, query in targets
        }
        for future in as_completed(futures):
            label = futures[future]
            try:
                results[label] = future.result()
            except Exception:
                results[label] = "（搜索失败）"

    # 尝试 Firecrawl 抓取搜索结果中的权威页面
    fc = _get_firecrawl()
    scraped_content = []
    if fc:
        # 从搜索结果中提取 URL，抓取前 3 个
        urls_to_scrape = []
        for label, content in results.items():
            for line in content.split("\n"):
                if "（来源：" in line:
                    url = line.split("（来源：")[1].rstrip("）")
                    if url.startswith("http"):
                        urls_to_scrape.append(url)

        unique_urls = list(dict.fromkeys(urls_to_scrape))[:3]  # 去重，最多3个
        for j, url in enumerate(unique_urls):
            try:
                result = fc.scrape_url(url, formats=["markdown"])
                md = result.markdown if hasattr(result, "markdown") else ""
                if md and len(md) > 200:
                    scraped_content.append(f"\n### 📄 权威源全文 #{j+1}: {url}\n{md[:3000]}")
            except Exception:
                pass

    # 组装输出
    lines = [f"## 🔬 权威源定向搜索结果：{entity_name}"]
    for label, _ in targets:
        content = results.get(label, "（搜索失败）")
        lines.append(f"\n### {label}\n{content}")

    if scraped_content:
        lines.append("\n---\n## 📄 权威源全文抓取")
        lines.extend(scraped_content)

    return "\n\n".join(lines)