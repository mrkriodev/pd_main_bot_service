from aiogram.utils.deep_linking import create_deep_link
from aiogram_dialog import DialogManager
from aiogram.types.update import Update
from service.users import UsersService
from utils import text as text_utils


async def get_profile(dialog_manager: DialogManager, **middleware_data):
    user_service: UsersService = middleware_data["user_service"]
    update: Update = middleware_data["event_update"]
    cq = update.callback_query
    user_id = cq.from_user.id
    lang = cq.from_user.language_code
    count_reff = await user_service.count_reff_users_by_user_id(user_id)
    username_bot = cq.message.from_user.username
    link = create_deep_link(
        username=username_bot, link_type="start", payload=str(user_id), encode=True
    )
    address = None
    return {
        "profile_text": text_utils.render_profile(
            lang, link=link, count_reff=count_reff, address=address
        ),
        "back_text": text_utils.back_button_label(lang),
    }
