from aiogram import md
from aiogram.types import Message, ReplyKeyboardRemove

from ..services import GetUrl
from ..texts import START


async def command_start(message: Message) -> None:
    await message.answer(
        text=START.format(
            full_name=md.quote_html(message.from_user.full_name),
            genres = ", ".join("/{url}".format(url=md.hbold(url)) for url in GetUrl.clear_genres)),
        parse_mode="HTML", disable_web_page_preview=True,
        reply_markup=ReplyKeyboardRemove(selective=True))
