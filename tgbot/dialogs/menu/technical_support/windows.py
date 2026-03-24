from aiogram.enums import ParseMode
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Format

from . import callbacks
from . import getters
from . import keyboards
from . import states


def technical_support():
    window = Window(
        Format("{support_text}"),
        keyboards.kbn_technical_support(callbacks.technical_support_callback),
        Cancel(Format("{back_text}")),
        state=states.TechnicalSupport.select_support,
        getter=getters.get_technical_support,
        parse_mode=ParseMode.HTML,
    )
    return window
