from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from service.users import UsersService
from utils.text import TEXT_WHEN_USER_SEND_PROBLEM_RU
from config import settings


async def technical_support_callback(m: Message, widget: Any, manager: DialogManager):
    user_service: UsersService = manager.middleware_data.get("user_service")
    await user_service.receive_message_from_user_help(m)
    await m.answer(TEXT_WHEN_USER_SEND_PROBLEM_RU)
    try:
        message_for_support = str(
            f"user id {m.from_user.id}\n" f"message from user: {m.text}\n"
        )
        await m.bot.send_message(
            chat_id=settings.bot.support_chat_id,
            text=message_for_support,
            #message_thread_id=settings.bot.support_thread_id,
        )
    except Exception as e:
        print(e)
        pass
    await manager.done()
