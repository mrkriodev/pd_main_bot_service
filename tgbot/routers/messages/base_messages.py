import logging

from aiogram import Router
from aiogram.types import Message

router = Router(name=__name__)


@router.message()
async def rec_message(message: Message):
    pass
