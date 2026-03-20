from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from utils.text import TEXT_TECHNICAL_SUPPORT_RU, TEXT_BACK_RU
from . import keyboards
from . import states
from . import callbacks


def technical_support():
    window = Window(
        TEXT_TECHNICAL_SUPPORT_RU,
        keyboards.kbn_technical_support(callbacks.technical_support_callback),
        Cancel(Const(TEXT_BACK_RU)),
        state=states.TechnicalSupport.select_support,
    )
    return window
