from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker


class DataBaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_poll: async_sessionmaker) -> None:
        self.session_pool = session_poll

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session_db"] = session
            return await handler(event, data)
