from aiogram import md
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.exceptions import BadRequest

from ..services import GetUrl
from ..texts import ACCESS_DENIED, GENRE_NOT_FOUND


async def command_get_url(message: Message, get_url: GetUrl) -> None:
    try:
        # get genre and ignore bot privacy mode
        text, *_ = message.text.split("@")
        # check genre for availability
        if text == "/":
            raise KeyError
        genre_with_prefix = text
        # ignore prefix
        genre = text[1:]
        url = await get_url.get_url(genre)
    # missing genre
    except KeyError:
        # available genres
        genres = ", ".join("/{url}".format(url=md.hbold(url)) for url in GetUrl.clear_genres)
        return await message.reply(GENRE_NOT_FOUND.format(genres=genres), parse_mode="HTML")
    # access denied
    if url is None:
        return await message.reply(ACCESS_DENIED, disable_web_page_preview=True)
    while True:
        try:
            await message.answer_photo(url,
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=[[KeyboardButton(genre_with_prefix)]],
                    resize_keyboard=True,
                    selective=True
                )
            )
        # incorrect url
        except BadRequest as exc:
            url = await get_url.get_url(genre)
        else:
            return
