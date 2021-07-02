from aiogram.types import Message

from ..texts import WHAT


async def command_what(message: Message) -> None:
    await message.reply(WHAT, disable_web_page_preview=True)
