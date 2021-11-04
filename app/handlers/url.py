import asyncio
import functools

from aiogram import types
from aiogram.utils import exceptions as tg_exceptions

from ..services import exceptions
from ..services.database import RedisDB
from ..services.urls import GetUrl
from ..utils import scripts
from ..utils import text as text_f


async def delele_error_message(message: types.Message):
    await message.delete()


async def command_sfw_get_url(
    message: types.Message,
    get_url: GetUrl,
    database: RedisDB,
):
    command = message.get_command(pure=True)
    genre_with_prefix, genre_without_prefix, \
        full = scripts.get_genre_and_mode(command=command)

    url_for_request = get_url.get_url_for_request(
        genre=genre_without_prefix,
    )
    received_urls = await database.get_received_urls(
        user_id=message.from_user.id,
    )
    try:
        url = await get_url.get_url_without_duplicates(
            url=url_for_request,
            received_urls=received_urls,
        )
    except exceptions.ManyDuplicates:
        text = text_f.get_text(
            language_code=message.from_user.language_code,
            text_name="many_duplicates",
        )
    except asyncio.TimeoutError:
        text = text_f.get_text(
            language_code=message.from_user.language_code,
            text_name="source_block",
        )
    else:
        await database.add_received_url(
            user_id=message.from_user.id,
            url=url,
        )
        text = None
    if text is None:
        markup = scripts.create_reply_keyboard_markup(
            keyboard=[
                [types.KeyboardButton("/start")],
                [types.KeyboardButton(genre_with_prefix),
                 types.KeyboardButton(f"{genre_with_prefix}_full")],
            ],
        )
        try:
            if full or url.endswith(".gif"):
                await message.answer_document(
                    document=url,
                    reply_markup=markup,
                )
            else:
                await message.answer_photo(
                    photo=url,
                    reply_markup=markup,
                )
        except (
            tg_exceptions.InvalidHTTPUrlContent,
            tg_exceptions.WrongFileIdentifier,
        ):
            return asyncio.get_event_loop().call_later(
                0.05, asyncio.create_task,
                command_sfw_get_url(
                    message=message,
                    get_url=get_url,
                    database=database,
                ),
            )
    else:
        error_message = await message.reply(text=text)

        asyncio.get_event_loop().call_later(
            10, asyncio.create_task,
            delele_error_message(
                message=error_message,
            ),
        )

    try:
        await message.delete()
    except tg_exceptions.MessageCantBeDeleted:
        pass


async def command_nsfw_get_url(message: types.Message):
    command = message.get_command(pure=True)
    genre_with_prefix, genre_without_prefix, \
        full = scripts.get_genre_and_mode(command=command)
    callback_data = f"{genre_with_prefix}:{genre_without_prefix}:{int(full)}"

    func = functools.partial(
        text_f.get_text,
        language_code=message.from_user.language_code,
    )

    await message.reply(
        text=func(text_name="confirmation"),
        reply_markup=scripts.create_inline_keyboard_markup(
            inline_keyboard=[[
                types.InlineKeyboardButton(
                    text=func(text_name="confirmation_keyboard"),
                    callback_data=callback_data,
                )
            ]],
        ),
    )

    try:
        await message.delete()
    except tg_exceptions.MessageCantBeDeleted:
        pass


async def command_send_nsfw_url(
    callback: types.CallbackQuery,
    get_url: GetUrl,
    database: RedisDB,
):
    await callback.answer()

    genre_with_prefix, genre_without_prefix, \
        full = callback.data.split(":")

    url_for_request = get_url.get_url_for_request(
        genre=genre_without_prefix,
    )
    received_urls = await database.get_received_urls(
        user_id=callback.from_user.id,
    )

    try:
        url = await get_url.get_url_without_duplicates(
            url=url_for_request,
            received_urls=received_urls,
        )
    except exceptions.ManyDuplicates:
        text = text_f.get_text(
            language_code=callback.from_user.language_code,
            text_name="many_duplicates",
        )
    except asyncio.TimeoutError:
        text = text_f.get_text(
            language_code=callback.from_user.language_code,
            text_name="source_block",
        )
    else:
        await database.add_received_url(
            user_id=callback.from_user.id,
            url=url,
        )
        text = None
    if text is None:
        markup = scripts.create_reply_keyboard_markup(
            keyboard=[
                [types.KeyboardButton("/start")],
                [types.KeyboardButton(genre_with_prefix),
                 types.KeyboardButton(f"{genre_with_prefix}_full")],
            ],
        )
        try:
            if full == "1" or url.endswith(".gif"):
                await callback.message.answer_document(
                    document=url,
                    reply_markup=markup,
                )
            else:
                await callback.message.answer_photo(
                    photo=url,
                    reply_markup=markup,
                )
        except (
            tg_exceptions.InvalidHTTPUrlContent,
            tg_exceptions.WrongFileIdentifier,
        ):
            asyncio.get_event_loop().call_later(
                0.05, asyncio.create_task,
                command_send_nsfw_url(
                    callback=callback,
                    get_url=get_url,
                    database=database,
                ),
            )
    else:
        error_message = await callback.message.reply(text=text)

        asyncio.get_event_loop().call_later(
            10, asyncio.create_task,
            delele_error_message(
                message=error_message,
            ),
        )
