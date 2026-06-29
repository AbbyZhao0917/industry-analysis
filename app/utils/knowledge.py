"""
知识库加载器 —— 加载 knowledge-base/ 目录下的 Markdown 文件
"""

import os

_KB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "knowledge-base")
_cache: dict[str, str] = {}


def get_kb_dir() -> str:
    return os.path.abspath(_KB_DIR)


def list_knowledge_files() -> list[str]:
    """列出所有知识库文件名（不含扩展名）"""
    files = []
    kb_dir = get_kb_dir()
    if os.path.isdir(kb_dir):
        for f in sorted(os.listdir(kb_dir)):
            if f.endswith(".md"):
                files.append(f.replace(".md", ""))
    return files


def load_knowledge(name: str) -> str:
    """按名称加载知识库文件内容"""
    if name in _cache:
        return _cache[name]

    filepath = os.path.join(get_kb_dir(), f"{name}.md")
    if not os.path.exists(filepath):
        return ""

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    _cache[name] = content
    return content


def load_all_knowledge() -> dict[str, str]:
    """加载全部知识库文件"""
    result = {}
    for name in list_knowledge_files():
        result[name] = load_knowledge(name)
    return result


def build_system_context(kb_names: list[str]) -> str:
    """将指定知识库文件拼接为系统提示上下文"""
    parts = [
        "## 方法论知识库\n",
        "以下内容来自肖璟《如何快速了解一个行业》(2025, 人民邮电出版社)：\n",
    ]
    for name in kb_names:
        content = load_knowledge(name)
        if content:
            parts.append(f"### {name}\n\n{content}\n\n---\n")
    return "\n".join(parts)