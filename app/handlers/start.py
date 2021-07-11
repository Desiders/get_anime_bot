from aiogram import md
from aiogram.types import Message, ReplyKeyboardRemove

from .. import texts
from ..utils.scripts import genres_format_text


async def command_start(message: Message):
    await message.answer(
        text=texts.START.format(
            full_name=md.quote_html(message.from_user.full_name),
            genres=genres_format_text()
        ),
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(selective=True)
    )
