import logging
from typing import Optional

from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram_dialog import DialogManager, StartMode, ShowMode

from dialogs.menu.main.states import BotMenu
from dialogs.menu.technical_support.states import TechnicalSupport
from filters.deep_links import FilterCustomLink
from schemas.users import UserMessageSchema
from service.users import UsersService

router = Router(name=__name__)


async def add_new_user(
    message: Message, user_service: UsersService, ref_id: Optional[int] = None
):
    user_data = UserMessageSchema(
        **(message.from_user.model_dump()), reff_user_id=ref_id
    )
    if ref_id is None:
        await user_service.add_new_user(user_data=user_data)
    else:
        await user_service.add_new_user_from_reff_user(user_data=user_data)


@router.message(CommandStart(deep_link=True), FilterCustomLink(link="shareorder_"))
async def shared_order(
    message: Message,
    command: CommandObject,
    user_service: UsersService,
):
    """Deep link /start shareorder_<bet_id>. Image is built only if the bet exists and
    belongs to the caller (enforced in BetDAO.get_order_of_user)."""
    order_id = command.args[len("shareorder_") :]
    user = await user_service.get_user(message.from_user.id)
    if user is None:
        return
    if order_id.isdigit():
        await user_service.create_shared_order(
            message=message,
            user_id=message.from_user.id,
            order_id=int(order_id),
        )
    await message.delete()


@router.message(CommandStart(deep_link=True), FilterCustomLink())
async def referral_user(
    message: Message,
    command: CommandObject,
    user_service: UsersService,
    dialog_manager: DialogManager,
):
    payload = None
    try:
        payload = int(decode_payload(command.args))
    except Exception as e:
        logging.error(e)
        logging.warning(f"{message.from_user.id} try crack link. Args: {command.args}")

    await add_new_user(message=message, user_service=user_service, ref_id=payload)

    await dialog_manager.start(
        BotMenu.select_main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
    await message.delete()


@router.message(CommandStart())
async def start(
    message: Message,
    user_service: UsersService,
    dialog_manager: DialogManager,
):
    await add_new_user(message=message, user_service=user_service)
    await dialog_manager.start(
        BotMenu.select_main_menu,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
    await message.delete()


@router.message(Command("support"))
async def support(
    message: Message,
    user_service: UsersService,
    dialog_manager: DialogManager,
):
    # Do not pre-create user here; support flow will create/check on first message.
    # Keep this command minimal to guarantee dialog state is entered.
    await dialog_manager.start(
        TechnicalSupport.select_support,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )
