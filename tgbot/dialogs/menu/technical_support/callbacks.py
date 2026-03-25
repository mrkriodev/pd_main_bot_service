import logging
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from service.users import UsersService
from utils import text as text_utils
from config import settings

logger = logging.getLogger(__name__)


async def technical_support_callback(m: Message, widget: Any, manager: DialogManager):
    logger.info(
        "technical_support_callback: start user_id=%s chat_id=%s message_id=%s text=%r",
        getattr(m.from_user, "id", None),
        getattr(m.chat, "id", None),
        m.message_id,
        m.text,
    )
    user_service: UsersService = manager.middleware_data.get("user_service")
    if user_service is None:
        logger.error("technical_support_callback: user_service is missing in middleware_data")
        return

    try:
        logger.info("technical_support_callback: saving support message to DB")
        await user_service.receive_message_from_user_help(m)
        logger.info("technical_support_callback: DB save committed")
    except Exception:
        logger.exception(
            "technical_support_callback: failed during DB save user_id=%s",
            getattr(m.from_user, "id", None),
        )
        raise

    try:
        ack_text = text_utils.support_message_ack(m.from_user.language_code)
        logger.info("technical_support_callback: sending ACK to user")
        await m.answer(ack_text)
        logger.info("technical_support_callback: ACK sent")
    except Exception:
        logger.exception(
            "technical_support_callback: failed to send ACK user_id=%s",
            getattr(m.from_user, "id", None),
        )
        raise

    try:
        message_for_support = str(
            f"user id {m.from_user.id}\n" f"message from user: {m.text}\n"
        )
        logger.info(
            "technical_support_callback: forwarding message to support_chat_id=%s",
            settings.bot.support_chat_id,
        )
        await m.bot.send_message(
            chat_id=settings.bot.support_chat_id,
            text=message_for_support,
            #message_thread_id=settings.bot.support_thread_id,
        )
        logger.info("technical_support_callback: forwarded to support chat")
    except Exception:
        logger.exception(
            "technical_support_callback: failed to forward to support chat_id=%s",
            settings.bot.support_chat_id,
        )

    await manager.done()
    logger.info("technical_support_callback: done")
