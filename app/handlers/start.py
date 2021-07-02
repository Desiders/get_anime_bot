from aiogram import md
from aiogram.types import Message

from ..services import GetUrl
from ..texts import START


async def command_start(message: Message) -> None:
    await message.answer(
        text=START.format(
            full_name=md.quote_html(message.from_user.full_name),
            genres=", ".join(f"/{md.hbold(url)}" for url in GetUrl.urls)),
        parse_mode="HTML", disable_web_page_preview=True
    )
