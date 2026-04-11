import socket

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.types import BotCommand

from config import settings
if settings.redis is not None:
    from storage.redis.redis_helper import redis_helper

storage = (
    MemoryStorage()
    if settings.redis is None
    else RedisStorage(
        redis_helper.get_redis(), key_builder=DefaultKeyBuilder(with_destiny=True)
    )
)


telegram_session = AiohttpSession()
# Force IPv4 to avoid broken IPv6 routing inside container.
telegram_session._connector_init["family"] = socket.AF_INET

bot = Bot(
    token=settings.bot.token,
    session=telegram_session,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(storage=storage)

bot_command = [
    BotCommand(command="start", description="Start bot"),
    BotCommand(command="support", description="Open support chat"),
]
