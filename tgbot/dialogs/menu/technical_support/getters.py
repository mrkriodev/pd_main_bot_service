from aiogram_dialog import DialogManager

from utils import text as text_utils


async def get_technical_support(dialog_manager: DialogManager, **kwargs):
    lang = None
    event = dialog_manager.event
    if getattr(event, "from_user", None):
        lang = event.from_user.language_code
    return {
        "support_text": text_utils.render_technical_support_prompt(lang),
        "back_text": text_utils.back_button_label(lang),
    }
