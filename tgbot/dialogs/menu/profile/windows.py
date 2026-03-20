from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from utils.text import TEXT_PROFILE_RU, TEXT_BACK_RU
from . import states
from . import getters


def profile():
    window = Window(
        TEXT_PROFILE_RU,
        Cancel(Const(TEXT_BACK_RU)),
        state=states.Profile.select_profile,
        getter=getters.get_profile,
    )
    return window
