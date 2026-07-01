"""
图表生成工具 —— 解析 LLM 输出的 chart 代码块，用 matplotlib 渲染为 PNG
"""
import re
import json
import base64
import io
from typing import Dict, List, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# ---- 中文字体设置 ----
def _setup_chinese_font():
    """探测可用的中文字体并设置"""
    candidates = [
        "PingFang SC", "Heiti SC", "STHeiti", "Songti SC",
        "Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei",
        "Noto Sans CJK SC", "Noto Sans SC",
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            return name
    # 回退：尝试 sans-serif
    plt.rcParams["font.family"] = "sans-serif"
    return "sans-serif"


_font_name = _setup_chinese_font()
plt.rcParams["axes.unicode_minus"] = False


# ---- 主接口 ----

def parse_charts(text: str) -> List[Dict]:
    """从报告文本中提取 ```chart 代码块"""
    pattern = r'```chart\s*\n(.*?)\n```'
    charts = []
    for match in re.finditer(pattern, text, re.DOTALL):
        try:
            data = json.loads(match.group(1))
            charts.append(data)
        except json.JSONDecodeError:
            continue
    return charts


def render_chart(chart_data: Dict) -> Optional[str]:
    """
    将 chart 数据渲染为 base64 PNG <img> 标签。

    支持的 type: bar, line, pie, radar
    必填字段: type, labels, values
    可选字段: title, xlabel, ylabel
    """
    chart_type = chart_data.get("type", "bar")
    labels = chart_data.get("labels", [])
    values = chart_data.get("values", [])
    title = chart_data.get("title", "")
    xlabel = chart_data.get("xlabel", "")
    ylabel = chart_data.get("ylabel", "")

    if not labels or not values:
        return None

    fig, ax = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor("#FAF9F7")
    ax.set_facecolor("#FAF9F7")

    color_palette = ["#2D5A4B", "#5A8F7A", "#8DB5A6", "#C4D9D0",
                     "#4A7C6B", "#6B9E8A", "#3D6B58", "#1F3D33"]

    try:
        if chart_type == "bar":
            bars = ax.bar(labels, values, color=color_palette[:len(labels)], edgecolor="white", linewidth=0.8)
            ax.set_xlabel(xlabel, color="#6B7280")
            ax.set_ylabel(ylabel, color="#6B7280")
            ax.tick_params(axis="x", rotation=25, colors="#2C3338")
            ax.tick_params(axis="y", colors="#2C3338")
            # 数值标签
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.01,
                        f"{val:,}", ha="center", va="bottom", fontsize=9, color="#2C3338")

        elif chart_type == "line":
            ax.plot(labels, values, color="#2D5A4B", marker="o", linewidth=2.2,
                    markersize=6, markerfacecolor="white", markeredgewidth=2, markeredgecolor="#2D5A4B")
            ax.fill_between(range(len(labels)), values, alpha=0.08, color="#2D5A4B")
            ax.set_xlabel(xlabel, color="#6B7280")
            ax.set_ylabel(ylabel, color="#6B7280")
            ax.tick_params(axis="x", rotation=25, colors="#2C3338")
            ax.tick_params(axis="y", colors="#2C3338")
            # 数值标签
            for i, val in enumerate(values):
                ax.text(i, val + max(values) * 0.02, f"{val:,}", ha="center", fontsize=9, color="#2C3338")

        elif chart_type == "pie":
            wedges, texts, autotexts = ax.pie(
                values, labels=None, autopct="%1.1f%%",
                colors=color_palette[:len(labels)],
                startangle=90, pctdistance=0.6,
                wedgeprops={"edgecolor": "white", "linewidth": 1.5},
            )
            for t in autotexts:
                t.set_fontsize(9)
                t.set_color("#2C3338")
            ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1, 0.5),
                      frameon=False, fontsize=9)
            # pie 不需要坐标轴标签
            xlabel, ylabel = "", ""

        elif chart_type == "radar":
            _render_radar(ax, labels, values, color_palette)
        else:
            plt.close(fig)
            return None

        if title:
            ax.set_title(title, fontsize=14, fontweight="600", color="#2C3338", pad=16)

        # 去掉顶部和右侧边框
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#E2E0DA")
        ax.spines["bottom"].set_color("#E2E0DA")

        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="#FAF9F7")
        plt.close(fig)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
        return f'<img src="data:image/png;base64,{b64}" class="report-chart" alt="{title}">'

    except Exception:
        plt.close(fig)
        return None


def _render_radar(ax, labels, values, colors):
    """雷达图"""
    import numpy as np
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_plot = values + values[:1]
    angles += angles[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9, color="#2C3338")
    ax.set_yticklabels([])

    ax.fill(angles, values_plot, color="#2D5A4B", alpha=0.15)
    ax.plot(angles, values_plot, color="#2D5A4B", linewidth=2, marker="o", markersize=5,
            markerfacecolor="white", markeredgewidth=2, markeredgecolor="#2D5A4B")

    ax.spines["polar"].set_color("#E2E0DA")
    ax.set_facecolor("#FAF9F7")


def embed_charts(html_body: str) -> str:
    """
    在 HTML 中查找 ```chart 代码块并替换为渲染后的 <img>。
    如果渲染失败，保留代码块原文（用 <pre> 包裹展示）。
    """
    def _replace(match):
        raw = match.group(0)
        json_str = match.group(1)
        try:
            data = json.loads(json_str)
            img_tag = render_chart(data)
            if img_tag:
                return img_tag
        except json.JSONDecodeError:
            pass
        # 回退：展示代码
        escaped = (json_str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        return f'<pre class="chart-fallback"><code>{escaped}</code></pre>'

    return re.sub(r'```chart\s*\n(.*?)\n```', _replace, html_body, flags=re.DOTALL)
