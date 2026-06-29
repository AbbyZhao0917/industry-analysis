"""联网搜索 —— DuckDuckGo 搜索最新数据（带重试）"""
import time
from duckduckgo_search import DDGS
from typing import Dict, List


def _ddg_search(query: str, max_results: int = 5) -> List[Dict]:
    """DuckDuckGo 搜索，带重试"""
    backends = ["html", "lite"]
    for attempt in range(3):
        backend = backends[attempt % 2]
        try:
            with DDGS(timeout=15) as ddgs:
                results = list(ddgs.text(query, max_results=max_results, backend=backend))
                if results:
                    return [
                        {
                            "title": r.get("title", ""),
                            "href": r.get("href", ""),
                            "body": r.get("body", ""),
                        }
                        for r in results
                    ]
        except Exception:
            time.sleep(2 * (attempt + 1))
    return []


def search_web(query: str, max_results: int = 5) -> str:
    """搜索网页并返回格式化结果"""
    results = _ddg_search(query, max_results)

    if not results:
        return "（联网搜索暂时不可用，分析将基于模型已有知识进行）"

    lines = []
    for i, r in enumerate(results, 1):
        lines.append(
            f"{i}. **{r['title']}**\n"
            f"   {r['body']}\n"
            f"   来源：{r['href']}"
        )

    return "\n\n".join(lines)


def search_for_industry(industry_name: str) -> str:
    """搜索行业最新数据"""
    return search_web(f"{industry_name} 行业 市场规模 2025 2026 趋势")


def search_for_company(company_name: str) -> str:
    """搜索企业最新数据"""
    return search_web(f"{company_name} 财报 营收 2025 经营数据")
