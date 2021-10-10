from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from .services.urls import GetUrl


class CheckCommandFilter(BoundFilter):
    key = "command_filter"

    def __init__(self, age_limit: str):
        self.is_sfw = age_limit == "sfw"

    async def check(self, message: Message) -> bool:
        command = message.get_command(pure=True)
        if command is None:
            return False

        command, *_ = command.lower().rsplit("_full", maxsplit=1)

        if self.is_sfw:
            return command in GetUrl.sfw_genres
        return command in GetUrl.nsfw_genres
