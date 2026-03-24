from aiogram.enums import ParseMode
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Format

from . import getters
from . import states


def profile():
    window = Window(
        Format("{profile_text}"),
        Cancel(Format("{back_text}")),
        state=states.Profile.select_profile,
        getter=getters.get_profile,
        parse_mode=ParseMode.HTML,
    )
    return window
