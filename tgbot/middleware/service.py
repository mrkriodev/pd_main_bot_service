from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from infrastructure.http_client import get_http_session
from service.users import UsersService


class InitServiceMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session = data["session_db"]
        data["user_service"] = UsersService(
            session=session,
            http_session=get_http_session(),
        )
        return await handler(event, data)
