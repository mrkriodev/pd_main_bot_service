# Кнопки для диалоговых окон
from aiogram.enums import ParseMode
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from . import getters
from . import keyboards
from .states import BotMenu


def main_menu():
    return Window(
        Format("{main_menu_text}"),
        keyboards.main_menu(),
        state=BotMenu.select_main_menu,
        getter=getters.get_main_menu_text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
