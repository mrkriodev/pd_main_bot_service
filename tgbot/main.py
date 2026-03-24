import asyncio
import logging

from aiogram import Bot
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState, OutdatedIntent
from aiohttp import web

from bot import bot, bot_command, dp
from config import settings
from dialogs import include_dialogs
from infrastructure.http_client import close_http_session, init_http_session
from dialogs.menu.error import on_unknown_intent, on_unknown_state
from middleware import register_global_middleware
from routers import router
from storage.postgres.db_helper import db_helper


async def on_startup_http_client(bot: Bot) -> None:
    await init_http_session()


async def on_shutdown_app_resources(bot: Bot) -> None:
    await close_http_session()
    await db_helper.dispose()


def register_functions():
    dp.startup.register(on_startup_http_client)
    dp.shutdown.register(on_shutdown_app_resources)
    register_global_middleware(dp=dp)

    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        on_unknown_state,
        ExceptionTypeFilter(UnknownState),
    )
    dp.errors.register(
        on_unknown_state,
        ExceptionTypeFilter(OutdatedIntent),
    )

    dp.include_router(router=router)

    include_dialogs(dp)
    setup_dialogs(dp)

    json_format = "{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}"
    logging.basicConfig(level=logging.INFO, format=json_format)


async def setup_menu_bot_commands():
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(
        commands=bot_command, scope=BotCommandScopeAllPrivateChats()
    )


async def run_polling():
    await setup_menu_bot_commands()
    await dp.start_polling(bot, skip_updates=True)


async def on_startup(bot: Bot) -> None:
    logging.info("Registration bot command")
    await setup_menu_bot_commands()

    logging.info("Registration webhook")
    await bot.set_webhook(
        f"{settings.bot.run_webhook.base_webhook_url}{settings.bot.run_webhook.webhook_path}",
        secret_token=settings.bot.run_webhook.webhook_secret,
    )


async def on_shutdown(bot: Bot) -> None:
    logging.info("Delete webhook")
    await bot.delete_webhook()


def run_webhook():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.bot.run_webhook.webhook_secret,
    )
    webhook_requests_handler.register(app, path=settings.bot.run_webhook.webhook_path)
    setup_application(app, dp, bot=bot)
    web.run_app(
        app,
        host=settings.bot.run_webhook.web_server_host,
        port=settings.bot.run_webhook.web_server_port,
    )


if __name__ == "__main__":
    register_functions()
    if settings.bot.run_polling is True:
        asyncio.run(run_polling())
    else:
        run_webhook()
