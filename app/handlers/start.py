from aiogram import md
from aiogram.types import Message, ReplyKeyboardRemove

from ..utils.scripts import get_text, sfw_genres_format_text


async def command_start(message: Message):
    text = get_text(lang_code=message.from_user.language_code, text_name="start")
    await message.answer(
        text=text.format(
            full_name=md.quote_html(message.from_user.full_name),
            sfw_genres=sfw_genres_format_text()
        ),
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(selective=True)
    )
