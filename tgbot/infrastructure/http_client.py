from __future__ import annotations

import asyncio

import aiohttp

from config import settings

_http_session: aiohttp.ClientSession | None = None
_http_session_lock = asyncio.Lock()


async def init_http_session() -> None:
    global _http_session
    async with _http_session_lock:
        if _http_session is not None and not _http_session.closed:
            return
        timeout = aiohttp.ClientTimeout(total=settings.main_backend.timeout_seconds)
        _http_session = aiohttp.ClientSession(timeout=timeout)


async def close_http_session() -> None:
    global _http_session
    if _http_session is not None and not _http_session.closed:
        await _http_session.close()
    _http_session = None


def get_http_session() -> aiohttp.ClientSession:
    if _http_session is None or _http_session.closed:
        raise RuntimeError(
            "aiohttp ClientSession is not ready; ensure init_http_session() runs on startup."
        )
    return _http_session


async def get_or_init_http_session() -> aiohttp.ClientSession:
    if _http_session is None or _http_session.closed:
        await init_http_session()
    return get_http_session()
