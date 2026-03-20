from aiogram_dialog import Dialog
from .main import windows
from .technical_support import windows as technical_support_windows
from .profile import windows as profile_windows


def bot_menu_dialogs():
    return [
        Dialog(
            windows.main_menu(),
        ),
        Dialog(technical_support_windows.technical_support()),
        Dialog(profile_windows.profile())
]
