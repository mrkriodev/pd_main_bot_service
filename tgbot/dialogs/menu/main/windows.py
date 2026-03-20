# Кнопки для диалоговых окон
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format

from .states import BotMenu
from . import keyboards
from utils.text import WELCOM_MESSAGE_RU


def main_menu():
    return Window(
        WELCOM_MESSAGE_RU,
        keyboards.main_menu(),
        state=BotMenu.select_main_menu,
        disable_web_page_preview=True,
    )
