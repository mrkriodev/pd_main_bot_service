from aiogram import Router
from routers.commands.base_commands import router as base_router_command
from routers.messages.base_messages import router as base_router_message

router = Router(name=__name__)

router.include_router(base_router_command)
router.include_router(base_router_message)
