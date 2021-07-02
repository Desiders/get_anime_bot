import logging

from aiogram import md
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.exceptions import BadRequest

from ..services import GetUrl
from ..texts import GENRE_NOT_FOUND

logger = logging.getLogger(__name__)

async def command_get_url(message: Message, get_url: GetUrl) -> None:
    try:
        user_input_genre = message.text
        if user_input_genre == "/":
            raise KeyError
        else:
            genre = user_input_genre[1:]
        url = await get_url.get_url(genre)
    except KeyError:
        genres = ", ".join(f"/{md.hbold(url)}" for url in GetUrl.urls)
        return await message.reply(GENRE_NOT_FOUND.format(genres=genres), parse_mode="HTML")
    while True:
        try:
            await message.answer_photo(url,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(user_input_genre)]],
                    resize_keyboard=True,
                    selective=True
                )
            )
        except BadRequest as exc:
            logger.error(exc)
        else:
            break
        url = await get_url.get_url(genre)
