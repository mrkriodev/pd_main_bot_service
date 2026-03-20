from aiogram.utils.deep_linking import create_deep_link
from aiogram.utils.link import create_telegram_link

from config import settings


def get_message_for_shared_order(user_id: int):
    link = create_deep_link(
        username=settings.bot.notification.username_bot,
        link_type="start",
        payload=str(user_id),
        encode=True,
    )

    link_channel = create_telegram_link(settings.bot.notification.username_channel)
    link_to_nft_market = settings.bot.notification.link_to_nft_market
    message = (
        f"🚀 Поделись со своими друзьями и получай сниженную комиссию навсегда:\n"
        f"<code>{link}</code>\n\n"
        f'🫶 Подпишись на наш <a href="{link_channel}">канал</a>:\n'
        f"{link_channel}"
        # f'\n\n🏬 Купить наше <a href="{link_to_nft_market}">NFT</a>:\n'
        # f"{link_to_nft_market}"
    )
    return message
