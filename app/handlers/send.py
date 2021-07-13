from aiogram.types import Message

from ..services.database import RedisDB
from ..utils.scripts import get_text


async def command_reset(message: Message, database: RedisDB):
    await database.clear_received_urls(user_id=message.from_user.id)

    text = get_text(lang_code=message.from_user.language_code, text_name="urls_reset")
    await message.reply(text=text)
