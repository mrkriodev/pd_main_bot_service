from aiogram.utils.deep_linking import create_deep_link
from aiogram_dialog import DialogManager
from aiogram.types.update import Update
from service.users import UsersService


async def get_profile(dialog_manager: DialogManager, **middleware_data):
    user_service: UsersService = middleware_data["user_service"]
    update: Update = middleware_data["event_update"]
    user_id = update.callback_query.from_user.id
    user = await user_service.get_user(user_id)
    count_reff = await user_service.count_reff_users_by_user_id(user_id)
    username_bot = update.callback_query.message.from_user.username
    data = {
        #"address": user.address,
        "link": create_deep_link(
            username=username_bot, link_type="start", payload=str(user_id), encode=True
        ),
        "count_reff": count_reff,
    }
    return data
