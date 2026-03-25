from aiogram import Router

router = Router(name=__name__)

# Historical fallback handler (disabled on purpose).
# It intercepted plain text and prevented dialog MessageInput handlers
# (like technical support flow) from receiving messages.
#
# import logging
# from aiogram.filters import StateFilter
# from aiogram.types import Message
#
# @router.message(StateFilter(None))
# async def rec_message(message: Message):
#     logging.info("Fallback message handler: no active state, message ignored")
