from aiogram import Router
from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, ShowMode, StartMode

from dialogs.menu.main.states import BotMenu

router = Router(name=__name__)

SHOW_MAIN_MENU_TEXT = "Show main menu"


@router.message(F.text == SHOW_MAIN_MENU_TEXT)
async def show_main_menu_from_reply_button(
    message: Message, dialog_manager: DialogManager
):
    await dialog_manager.start(
        BotMenu.select_main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
    await message.answer(reply_markup=ReplyKeyboardRemove())

# Historical fallback handler (disabled on purpose).
# It intercepted plain text and prevented dialog MessageInput handlers
# (like technical support flow) from receiving messages.
#
# import logging
# from aiogram.filters import StateFilter
# from aiogram.types import Message
#
# @router.message(StateFilter(None))
# async def rec_message(message: Message):
#     logging.info("Fallback message handler: no active state, message ignored")
