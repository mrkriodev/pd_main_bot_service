import logging

from aiogram.enums import ParseMode

from bot import bot


class MessageBotService:
    @staticmethod
    async def send_notification_for_user_from_bot(user_id: int, message: str):
        try:
            result = await bot.send_message(
                chat_id=user_id, text=message, parse_mode=ParseMode.HTML
            )
            logging.info(
                f"Bot send message user_id: {user_id} | message_id: {result.message_id} | message: {message}"
            )
            await bot.session.close()
            return True
        except Exception as e:
            logging.error(e)
        return False

    @staticmethod
    async def send_notification_with_photo_for_user(user_id: int, photo, caption: str):
        try:
            result = await bot.send_photo(
                chat_id=user_id, photo=photo, caption=caption, parse_mode=ParseMode.HTML
            )
            logging.info(
                f"Bot send photo user_id: {user_id} | message_id: {result.message_id}"
            )
            await bot.session.close()
            return True
        except Exception as e:
            logging.error(e)
        return False
