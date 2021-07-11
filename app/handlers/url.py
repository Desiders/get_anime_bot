import asyncio
import logging

from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.exceptions import BadRequest

from .. import texts
from ..services import exceptions
from ..services.database import RedisDB
from ..services.urls import GetUrl
from ..utils.scripts import genres_format_text, get_genre_and_mode

logger = logging.getLogger(__name__)


async def command_get_url(message: Message, get_url: GetUrl, database: RedisDB):
    text, *_ = message.text.split("@")
    if text == "/":
        text = texts.GENRE_NOT_FOUND.format(genres=genres_format_text())
    else:
        genre_with_prefix, genre_without_prefix, full = get_genre_and_mode(text)
        try:
            url = get_url.get_url_for_request(genre=genre_without_prefix)
        except exceptions.UncnownGenre:
            text = texts.GENRE_NOT_FOUND.format(genres=genres_format_text())
        else:
            received_urls = await database.get_received_urls(user_id=message.from_user.id)
            try:
                url = await get_url.get_url_without_duplicates(url=url, received_urls=received_urls)
            except exceptions.UrlNotFound:
                await database.clear_received_urls(user_id=message.from_user.id)

                text = texts.URL_NOT_FOUND
            except exceptions.SourceBlock:
                text = texts.SOURCE_BLOCK
            else:
                await database.add_received_url(user_id=message.from_user.id, url=url)

                text = None
    if text is None:
        try:
            markup = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(genre_with_prefix),
                     KeyboardButton(f"{genre_with_prefix}_full")]
                ],
                resize_keyboard=True,
                selective=True
            )
            if full:
                await message.answer_document(document=url, reply_markup=markup)
            else:
                await message.answer_photo(photo=url, reply_markup=markup)
        except BadRequest as exc:
            await asyncio.sleep(1)
            await command_get_url(message, get_url, database)
    else:
        await message.reply(text=text, parse_mode="HTML")
