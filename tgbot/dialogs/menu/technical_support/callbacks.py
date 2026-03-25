import logging
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from service.users import UsersService
from utils import text as text_utils
from config import settings

logger = logging.getLogger(__name__)


async def technical_support_callback(m: Message, widget: Any, manager: DialogManager):
    user_service: UsersService = manager.middleware_data.get("user_service")
    if user_service is None:
        logger.error("user_service is missing in middleware_data")
        return

    await user_service.receive_message_from_user_help(m)
    await m.answer(text_utils.support_message_ack(m.from_user.language_code))

    try:
        message_for_support = str(
            f"user id {m.from_user.id}\n" f"message from user: {m.text}\n"
        )
        await m.bot.send_message(
            chat_id=settings.bot.support_chat_id,
            text=message_for_support,
            #message_thread_id=settings.bot.support_thread_id,
        )
    except Exception:
        logger.exception("Failed to forward support message to support chat")

    await manager.done()
