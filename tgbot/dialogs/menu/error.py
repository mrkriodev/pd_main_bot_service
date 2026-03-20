import logging

from aiogram.types import Message, ErrorEvent

from .main.states import BotMenu
from aiogram_dialog import DialogManager, StartMode, ShowMode


async def on_unknown_intent(event, dialog_manager: DialogManager):
    # Example of handling UnknownIntent Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        BotMenu.select_main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )


async def on_unknown_state(event, dialog_manager: DialogManager):
    # Example of handling UnknownState Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    await dialog_manager.start(
        BotMenu.select_main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
