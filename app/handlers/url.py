import asyncio
import functools

from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton, Message,
                           ReplyKeyboardMarkup)
from aiogram.utils.exceptions import WrongFileIdentifier

from ..services import exceptions
from ..services.database import RedisDB
from ..services.urls import GetUrl
from ..utils.scripts import get_genre_and_mode, get_text


async def command_sfw_get_url(message: Message, get_url: GetUrl, database: RedisDB):
    command = message.get_command(pure=True)
    genre_with_prefix, genre_without_prefix, full = get_genre_and_mode(command=command)

    url_for_request = get_url.get_url_for_request(genre=genre_without_prefix)
    received_urls = await database.get_received_urls(user_id=message.from_user.id)
    try:
        url = await get_url.get_url_without_duplicates(url=url_for_request, received_urls=received_urls)
    except exceptions.UrlNotFound:
        await database.clear_received_urls(user_id=message.from_user.id)

        text = get_text(lang_code=message.from_user.language_code, text_name="url_not_found")
    except exceptions.SourceBlock:
        text = get_text(lang_code=message.from_user.language_code, text_name="source_block")
    else:
        await database.add_received_url(user_id=message.from_user.id, url=url)

        text = None
    if text is None:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("/start")],
                [KeyboardButton(genre_with_prefix), KeyboardButton(f"{genre_with_prefix}_full")]
            ],
            resize_keyboard=True,
            selective=True
        )
        try:
            if full or url.endswith(".gif"):
                await message.answer_document(document=url, reply_markup=markup)
            else:
                await message.answer_photo(photo=url, reply_markup=markup)
        except WrongFileIdentifier:
            await asyncio.sleep(1)
            await command_sfw_get_url(message, get_url, database)
    else:
        await message.reply(text=text, parse_mode="HTML")


async def command_nsfw_get_url(message: Message):
    command = message.get_command(pure=True)
    genre_with_prefix, genre_without_prefix, full = get_genre_and_mode(command=command)
    callback_data = f"{genre_with_prefix}:{genre_without_prefix}:{int(full)}"

    func = functools.partial(get_text, lang_code=message.from_user.language_code)
    text = func(text_name="confirmation")
    text_keyboard = func(text_name="confirmation_keyboard")

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text_keyboard,
                                  callback_data=callback_data)
            ]
        ]
    )
    await message.reply(text=text, reply_markup=markup)


async def command_send_nsfw_url(callback: CallbackQuery, get_url: GetUrl, database: RedisDB):
    genre_with_prefix, genre_without_prefix, full = callback.data.split(":")

    url_for_request = get_url.get_url_for_request(genre=genre_without_prefix)
    received_urls = await database.get_received_urls(user_id=callback.from_user.id)
    try:
        url = await get_url.get_url_without_duplicates(url=url_for_request, received_urls=received_urls)
    except exceptions.UrlNotFound:
        await database.clear_received_urls(user_id=callback.from_user.id)

        text = get_text(lang_code=callback.from_user.language_code, text_name="url_not_found")
    except exceptions.SourceBlock:
        text = get_text(lang_code=callback.from_user.language_code, text_name="source_block")
    else:
        await database.add_received_url(user_id=callback.from_user.id, url=url)

        text = None
    if text is None:
        markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("/start")],
                [KeyboardButton(genre_with_prefix), KeyboardButton(f"{genre_with_prefix}_full")]
            ],
            resize_keyboard=True,
            selective=True
        )
        try:
            if full == "1" or url.endswith(".gif"):
                await callback.message.answer_document(document=url, reply_markup=markup)
            else:
                await callback.message.answer_photo(photo=url, reply_markup=markup)
        except WrongFileIdentifier:
                await asyncio.sleep(1)
                await command_send_nsfw_url(callback, get_url, database)
    else:
        await callback.message.reply(text=text, parse_mode="HTML")
    await callback.answer()
