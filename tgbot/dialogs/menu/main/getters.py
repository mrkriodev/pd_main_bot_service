from aiogram_dialog import DialogManager

from utils import text as text_utils


async def get_main_menu_text(dialog_manager: DialogManager, **kwargs):
    lang = None
    event = dialog_manager.event
    if getattr(event, "from_user", None):
        lang = event.from_user.language_code
    return {"main_menu_text": text_utils.render_welcome(lang)}
