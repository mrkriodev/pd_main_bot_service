from aiogram import Dispatcher
from . import menu


def include_dialogs(dp: Dispatcher):
    for dialog in [
        *menu.bot_menu_dialogs(),
    ]:
        dp.include_router(dialog)  # register a dialog
