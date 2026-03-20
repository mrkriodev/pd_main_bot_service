import json

from aiogram.utils.deep_linking import create_deep_link
from aiogram.utils.link import create_telegram_link
from models.notification import Notification

from schemas.notifications import OrderNotificationSchema
from config import settings


class ConvertNotificationToMessage:
    @staticmethod
    def order_info_to_message(notification: OrderNotificationSchema):
        message = (
            f"Ордеру №{notification.order_id}\n"
            f"Присвоен статус: {notification.status}"
        )

        return message

    @staticmethod
    def shared_link_to_message(notification: Notification):
        link = create_deep_link(
            username=settings.bot.notification.username_bot,
            link_type="start",
            payload=str(notification.user_id),
            encode=True,
        )

        link_channel = create_telegram_link(settings.bot.notification.username_channel)
        link_to_nft_market = settings.bot.notification.link_to_nft_market
        message = (
            f"🚀 Поделись со своими друзьями и получай сниженную комиссию навсегда:\n"
            f"<code>{link}</code>\n\n"
            f"🫶 Подпишись на наш канал:\n"
            f"{link_channel}\n\n"
            # f"\n\n🏬 Купить наше NFT:\n"
            # f"{link_to_nft_market}"
        )
        return message

    @staticmethod
    def broadcast_to_message(notification: Notification):
        info: dict = json.loads(notification.message)
        message = f"Реклама упс!"

        return message
