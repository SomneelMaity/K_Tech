"""Shared Anthropic client for the strategy and copy stages."""

from typing import Optional

from anthropic import AsyncAnthropic

from ..config import settings

_client: Optional[AsyncAnthropic] = None


def get_client() -> AsyncAnthropic:
    global _client
    if _client is None:
        _client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _client
