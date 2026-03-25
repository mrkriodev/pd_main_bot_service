import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from dialogs.menu.technical_support.states import TechnicalSupport
from dialogs.menu.profile.states import Profile

logger = logging.getLogger(__name__)


async def click_btn_technical_support(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    logger.info(
        "click_btn_technical_support: user_id=%s chat_id=%s callback_data=%r",
        callback.from_user.id,
        callback.message.chat.id if callback.message else None,
        callback.data,
    )
    await callback.answer()
    await manager.start(state=TechnicalSupport.select_support)
    logger.info(
        "click_btn_technical_support: started state=%s for user_id=%s",
        TechnicalSupport.select_support.state,
        callback.from_user.id,
    )


async def click_btn_profile(
    callback: CallbackQuery, button: Button, manager: DialogManager
):
    await callback.answer()
    await manager.start(state=Profile.select_profile)
