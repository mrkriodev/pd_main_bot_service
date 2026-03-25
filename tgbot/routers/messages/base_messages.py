import logging

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router(name=__name__)


#router.message()
@router.message(StateFilter(None))
async def rec_message(message: Message):
    #pass
    logging.info("Fallback message handler: no active state, message ignored")
