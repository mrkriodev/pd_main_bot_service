from aiogram_dialog.widgets.kbd import Group, Button, WebApp, Row
from aiogram_dialog.widgets.text import Const
from config import settings

from . import callbacks


def main_menu():

    keys = Group(
        Row(
            WebApp(
                Const("📈 Make Bet"), id="webapp_start", url=Const(settings.bot.webapp)
            ),
            # WebApp(
            #     Const("💼 My Profile"),
            #     id="webapp_order_list",
            #     url=Const(f"{settings.bot.webapp}/profile"),
            # ),
        ),
        # Row(
        #     WebApp(
        #         Const("💼 My Achives"),
        #         id="webapp_order_list",
        #         url=Const(f"{settings.bot.webapp}/profile"),
        #     ),
        # ),
        # Row(
        #     Button(
        #         Const("👤 Invite friend"),
        #         id="make_referral_link",
        #         on_click=callbacks.click_btn_make_referral_link,
        #     )
        # ),
        # Row(
        #     WebApp(
        #         Const("🏆 Rewards"),
        #         id="webapp_rewards",
        #         url=Const(f"{settings.bot.webapp}/rewards"),
        #     )
        # ),
        # Row(
        #     WebApp(
        #         Const("🤖 Robot"),
        #         id="webapp_robot",
        #         url=Const(f"{settings.bot.webapp}/robot"),
        #     ),
        # ),
        Row(
            Button(
                Const("👤 Profile"),
                id="profile",
                on_click=callbacks.click_btn_profile,
            )
        ),
        # Row(
        #     WebApp(
        #         Const("⌨️ AIChat"),
        #         id="webapp_aichat",
        #         url=Const(f"{settings.bot.webapp}/webapp/aichat"),
        #     )
        # ),
        # External support bot link (kept for reference):
        # Row(
        #     Url(
        #         Const("🆘 Support"),
        #         url=Const("https://t.me/pumdump_support_bot?start"),
        #     )
        # ),
        Row(
            Button(
                Const("🆘 Support"),
                id="technical_support",
                on_click=callbacks.click_btn_technical_support,
            )
        ),
    )

    return keys
