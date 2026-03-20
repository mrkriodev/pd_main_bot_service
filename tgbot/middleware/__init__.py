from aiogram import Dispatcher

from middleware.logging import LoggingMiddleware
from middleware.service import InitServiceMiddleware
from middleware.session import DataBaseSessionMiddleware
from storage.postgres.db_helper import db_helper


def register_global_middleware(dp: Dispatcher):
    dp.update.outer_middleware(LoggingMiddleware())
    dp.update.outer_middleware(DataBaseSessionMiddleware(db_helper.session_factory))
    dp.update.middleware(InitServiceMiddleware())
