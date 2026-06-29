"""
Claude API 客户端封装
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

_client = None


def get_client() -> anthropic.Anthropic:
    """获取 Anthropic 客户端单例"""
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("未设置 ANTHROPIC_API_KEY，请在 .env 文件中配置")
        base_url = os.getenv("ANTHROPIC_BASE_URL")
        if base_url:
            _client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
        else:
            _client = anthropic.Anthropic(api_key=api_key)
    return _client


def get_model() -> str:
    return os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


def ask_claude(system_prompt: str, user_message: str, max_tokens: int = 8000) -> str:
    """发送请求到 Claude API"""
    client = get_client()
    message = client.messages.create(
        model=get_model(),
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
        thinking={"type": "disabled"},
    )
    return message.content[0].text