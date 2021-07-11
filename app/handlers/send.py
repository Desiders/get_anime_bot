from aiogram.types import Message

from .. import texts
from ..services.database import RedisDB


async def command_reset(message: Message, database: RedisDB):
    await database.clear_received_urls(user_id=message.from_user.id)
    await message.reply(text=texts.URLS_RESET)


async def command_what(message: Message):
    await message.reply(text=texts.WHAT)
