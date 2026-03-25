from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button

from dialogs.menu.technical_support.states import TechnicalSupport
from dialogs.menu.profile.states import Profile


async def click_btn_technical_support(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await callback.answer()
    await manager.start(
        state=TechnicalSupport.select_support,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


async def click_btn_profile(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await callback.answer()
    await manager.start(state=Profile.select_profile)
