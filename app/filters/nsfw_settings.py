from aiogram.dispatcher.filters import Filter
from aiogram.types.base import TelegramObject
from app.infrastructure.database.models import UserModel


class NSFWSettings(Filter):
    def __init__(self, can_show_nsfw: bool):
        self.can_show_nsfw = can_show_nsfw

    async def check(self, obj: TelegramObject) -> bool:
        user: UserModel = obj.bot["user"]

        return user.show_nsfw is self.can_show_nsfw
