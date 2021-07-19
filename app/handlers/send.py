from aiogram.types import Message

from ..services.database import RedisDB
from ..utils.text import get_text


async def command_reset(message: Message, database: RedisDB):
    await database.clear_received_urls(user_id=message.from_user.id)
    await message.reply(
        text=get_text(
            language_code=message.from_user.language_code,
            text_name="urls_reset"
        )
    )
