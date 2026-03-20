import asyncio
import logging
from typing import Optional

from aiogram import types
from models.notification import Notification, StatusNotification
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.notifications import (
    TypeNotificationSchema,
    TypeNotificationEnum,
    SharedLinkNotificationSchema,
    OrderNotificationSchema,
)
from service.bot_message import MessageBotService
from storage.postgres.dao.notifications import NotificationDAO
from storage.postgres.dao.users import UserDAO
from storage.postgres.db_helper import db_helper
from utils.generator_images.generator import GeneratorHTML
from utils.notifications import ConvertNotificationToMessage

from config import settings

json_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
logging.basicConfig(level=logging.INFO, format=json_format)


class ProcessingNotification(
    ConvertNotificationToMessage, MessageBotService, GeneratorHTML
):

    async def process_notification_order(self, notification: Notification):
        info = OrderNotificationSchema.parse_raw(notification.message)
        message = self.order_info_to_message(info)
        return await self.send_notification_for_user_from_bot(
            user_id=notification.user_id, message=message
        )

    async def process_notification_shared_order(self, notification: Notification):
        info = SharedLinkNotificationSchema.parse_raw(notification.message)
        html = self.generate_html_shared_result_order(
            pair=info.pair,
            result=info.result,
            profit=info.profit,
            open_order=info.open_order,
            close_close=info.close_order,
        )
        file_name = await self.save_html(html)
        url_to_html_from_server = f"{settings.bot.notification.link_to_img}/{file_name}"
        message = self.shared_link_to_message(notification)
        print(f"url_to_html_from_server: {url_to_html_from_server}")
        image_bytes = await self.get_image(url_to_html_from_server)
        if image_bytes is not None:
            input_file = types.BufferedInputFile(file=image_bytes, filename="image.png")
        else:
            return False

        return await self.send_notification_with_photo_for_user(
            user_id=notification.user_id,
            photo=input_file,
            caption=message,
        )

    async def process_broadcast_notification(self, notification: Notification):
        return None


class NotificationService(ProcessingNotification):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session
        self.notification_dao = NotificationDAO(session)
        self.user_dao = UserDAO(session)

    async def do_when_notification_is_sending(
        self, status: Optional[bool], notification: Notification
    ):
        if status is True:
            await self.notification_dao.update_notification_status(
                notification_id=notification.id,
                status=StatusNotification.DELIVERED,
            )
        elif status is False:
            await self.notification_dao.update_notification_status(
                notification_id=notification.id,
                status=StatusNotification.ERROR,
            )
        else:
            await self.notification_dao.update_notification_status(
                notification_id=notification.id,
                status=StatusNotification.UNKNOWN,
            )
        await self.session.commit()

    async def get_notification_for_bot_and_send(self):
        list_notification = await self.notification_dao.get_all_created_notifications()

        for notification in list_notification:
            type_notification = TypeNotificationSchema.parse_raw(notification.message)
            match type_notification.type:
                case TypeNotificationEnum.order:
                    status = await self.process_notification_order(notification)
                case TypeNotificationEnum.shared_link:
                    status = await self.process_notification_shared_order(notification)
                case TypeNotificationEnum.broadcast_message:
                    status = await self.process_broadcast_notification(notification)

                case None:
                    status = None
                case _:
                    status = None

            await self.do_when_notification_is_sending(
                status=status, notification=notification
            )


async def run_notification_service():
    logging.info("Start service...")
    while True:
        async with db_helper.session_factory() as session:
            notification_service = NotificationService(session=session)
            await notification_service.get_notification_for_bot_and_send()
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(run_notification_service())
