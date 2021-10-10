from aiogram import types

from ..services.database import RedisDB
from ..utils import text


async def command_reset(message: types.Message, database: RedisDB):
    await database.clear_received_urls(user_id=message.from_user.id)

    await message.reply(
        text=text.get_text(
            language_code=message.from_user.language_code,
            text_name="urls_reset",
        )
    )
