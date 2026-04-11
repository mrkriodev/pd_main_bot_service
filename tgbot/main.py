import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramNetworkError
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState, OutdatedIntent
from aiohttp import ClientSession, ClientTimeout, web

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


async def _check_tcp_connectivity(host: str, port: int, timeout_seconds: float = 3.0) -> bool:
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout_seconds,
        )
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False


async def _check_api_telegram_org(timeout_seconds: float = 5.0) -> bool:
    try:
        timeout = ClientTimeout(total=timeout_seconds)
        async with ClientSession(timeout=timeout) as session:
            async with session.get("https://api.telegram.org") as resp:
                return 200 <= resp.status < 500
    except Exception:
        return False


async def _startup_network_checks() -> None:
    telegram_ok, dns_ok = await asyncio.gather(
        _check_api_telegram_org(),
        _check_tcp_connectivity("8.8.8.8", 53),
    )
    logging.info("Startup network check api.telegram.org: %s", telegram_ok)
    logging.info("Startup network check 8.8.8.8:53: %s", dns_ok)
    if not telegram_ok:
        logging.error("api.telegram.org is not reachable from container")
    if not dns_ok:
        logging.error("8.8.8.8:53 is not reachable from container")


async def _retry_telegram_call(
    action_name: str,
    call,
    *,
    attempts: int = 5,
    base_delay_seconds: float = 2.0,
) -> bool:
    for attempt in range(1, attempts + 1):
        try:
            await call()
            return True
        except TelegramNetworkError:
            logging.exception(
                "%s failed due to network timeout (attempt %s/%s)",
                action_name,
                attempt,
                attempts,
            )
        except TelegramAPIError:
            logging.exception(
                "%s failed due to Telegram API error (attempt %s/%s)",
                action_name,
                attempt,
                attempts,
            )
            break

        if attempt < attempts:
            await asyncio.sleep(base_delay_seconds * attempt)

    logging.error("%s failed after %s attempt(s)", action_name, attempts)
    return False


async def run_polling():
    await _startup_network_checks()
    await _retry_telegram_call(
        "Registration bot command",
        setup_menu_bot_commands,
    )
    await dp.start_polling(bot, skip_updates=True)


async def on_startup(bot: Bot) -> None:
    await _startup_network_checks()
    logging.info("Registration bot command")
    await _retry_telegram_call(
        "Registration bot command",
        setup_menu_bot_commands,
    )

    logging.info("Registration webhook")
    webhook_url = (
        f"{settings.bot.run_webhook.base_webhook_url}"
        f"{settings.bot.run_webhook.webhook_path}"
    )
    await _retry_telegram_call(
        "Registration webhook",
        lambda: bot.set_webhook(
            webhook_url,
            secret_token=settings.bot.run_webhook.webhook_secret,
        ),
    )


async def on_shutdown(bot: Bot) -> None:
    logging.info("Delete webhook")
    try:
        await bot.delete_webhook()
    except (TelegramNetworkError, TelegramAPIError):
        logging.exception("Failed to delete webhook during shutdown")


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
