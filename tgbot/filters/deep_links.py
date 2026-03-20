from typing import Optional

from aiogram.filters import BaseFilter, CommandObject
from aiogram.types import Message


class FilterCustomLink(BaseFilter):
    def __init__(self, link: Optional[str] = None):
        self.link = link

    async def __call__(self, message: Message, command: CommandObject) -> bool:
        if not command.args:
            return False
        if self.link and not command.args.startswith(self.link):
            return False
        return True
