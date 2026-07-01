"""联网搜索 —— 多后端 + 代理支持"""
import os
import re
import time
import requests
from typing import List, Dict


def _get_proxies() -> dict | None:
    """读取代理配置"""
    proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
    if proxy:
        return {"http": proxy, "https": proxy}
    return None


def _ddg_html(query: str, max_results: int, proxies) -> List[Dict]:
    """DuckDuckGo HTML 后端"""
    try:
        r = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"},
            timeout=15,
            proxies=proxies,
        )
        if r.status_code != 200:
            return []
        html = r.text
    except Exception:
        return []

    results = []
    # DDG HTML 用 class="result__body" 包裹每条结果
    blocks = re.split(r'class="result__body"', html)[1 : max_results + 1]

    for block in blocks:
        title_m = re.search(r'class="result__title"[^>]*>.*?<a[^>]*>(.*?)</a>', block, re.DOTALL)
        snippet_m = re.search(r'class="result__snippet"[^>]*>(.*?)</', block, re.DOTALL)
        url_m = re.search(r'class="result__url"[^>]*>(.*?)</', block, re.DOTALL)

        title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else ""
        snippet = re.sub(r"<[^>]+>", "", snippet_m.group(1)).strip() if snippet_m else ""
        url = re.sub(r"<[^>]+>", "", url_m.group(1)).strip() if url_m else ""

        if title and snippet:
            results.append({"title": title, "href": url, "body": snippet[:300]})

    return results


def _ddg_lite(query: str, max_results: int, proxies) -> List[Dict]:
    """DuckDuckGo Lite 后端"""
    try:
        r = requests.get(
            "https://lite.duckduckgo.com/lite/",
            params={"q": query},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
            proxies=proxies,
        )
        if r.status_code != 200:
            return []
        html = r.text
    except Exception:
        return []

    results = []
    # Lite 用简单的 table 结构
    links = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', html)
    snippets = re.findall(r'<td class="result-snippet"[^>]*>(.*?)</td>', html, re.DOTALL)

    for i, (url, title_raw) in enumerate(links):
        title = re.sub(r"<[^>]+>", "", title_raw).strip()
        if len(title) < 10 or "duckduckgo" in url:
            continue
        if len(results) >= max_results:
            break
        snippet = re.sub(r"<[^>]+>", "", snippets[i]).strip() if i < len(snippets) else ""
        results.append({"title": title, "href": url, "body": snippet[:300]})

    return results


def search_web(query: str, max_results: int = 5) -> str:
    """联网搜索，返回格式化结果"""
    proxies = _get_proxies()

    # 依次尝试不同后端
    for backend, fn in [("DDG HTML", _ddg_html), ("DDG Lite", _ddg_lite)]:
        try:
            results = fn(query, max_results, proxies)
            if results:
                break
        except Exception:
            time.sleep(1)
    else:
        results = []

    if not results:
        return "（联网搜索不可用，以下数据来自模型训练知识。标注链接为已知权威来源格式，建议自行核验最新数据。）"

    lines = []
    for i, r in enumerate(results, 1):
        url_str = f"（来源：{r['href']}）" if r["href"] else ""
        lines.append(f"{i}. **{r['title']}**\n   {r['body']} {url_str}")

    return "\n\n".join(lines)


def search_for_industry(industry_name: str) -> str:
    return search_web(f"{industry_name} 行业 市场规模 2025 2026")


def search_for_company(company_name: str) -> str:
    return search_web(f"{company_name} 财报 营收 经营数据 2025")
