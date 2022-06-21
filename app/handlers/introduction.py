import html
from itertools import chain

from aiogram import Dispatcher
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram_dialog import DialogManager, StartMode
from app.dialogs import Language, Settings
from app.infrastructure.database.models import UserModel
from app.infrastructure.media import MediaSource
from app.typehints import I18nGettext


async def start_cmd(m: Message, _: I18nGettext):
    first_name = html.escape(m.from_user.first_name)

    text = _(
        "Hello, {first_name}!\n\n"
        "Get an anime GIF or image by genre!\n"
        "/genres_gif\n"
        "/genres_img\n"
        "/genres_all (can return gif and image)\n\n"
        "/language — change language\n"
        "/settings — change settings"
    ).format(
        first_name=first_name,
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        disable_notification=False,
        reply_markup=ReplyKeyboardRemove(),
    )


async def genres_gif_cmd(
    m: Message,
    _: I18nGettext,
    sources: set[MediaSource],
    user: UserModel,
):
    if user.show_nsfw:
        genres = list(chain.from_iterable(
            source.genres_gif
            for source in sources
        ))
    else:
        genres = list(chain.from_iterable(
            source.sfw_genres_gif
            for source in sources
        ))
    genres.sort()

    text = _(
        "Available genres:\n\n{genres}"
    ).format(
        genres=" ".join(map(lambda string: "/" + string, genres)),
    )

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True,
        row_width=1,
        keyboard=[
            [KeyboardButton(text="/help")],
        ],
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        disable_notification=False,
        reply_markup=markup,
    )


async def genres_img_cmd(
    m: Message,
    _: I18nGettext,
    sources: set[MediaSource],
    user: UserModel,
):
    if user.show_nsfw:
        genres = list(chain.from_iterable(
            source.genres_img
            for source in sources
        ))
    else:
        genres = list(chain.from_iterable(
            source.sfw_genres_img
            for source in sources
        ))
    genres.sort()

    text = _(
        "Available genres:\n\n{genres}"
    ).format(
        genres=" ".join(map(lambda string: "/" + string, genres)),
    )

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True,
        row_width=1,
        keyboard=[
            [KeyboardButton(text="/help")],
        ],
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        disable_notification=False,
        reply_markup=markup,
    )


async def genres_all_cmd(
    m: Message,
    _: I18nGettext,
    sources: set[MediaSource],
    user: UserModel,
):
    if user.show_nsfw:
        genres = list(chain.from_iterable(
            source.genres_all
            for source in sources
        ))
    else:
        genres = list(chain.from_iterable(
            source.sfw_genres_all
            for source in sources
        ))
    genres.sort()

    text = _(
        "Available genres:\n\n{genres}"
    ).format(
        genres=" ".join(map(lambda string: "/" + string, genres)),
    )

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True,
        row_width=1,
        keyboard=[
            [KeyboardButton(text="/help")],
        ],
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        disable_notification=False,
        reply_markup=markup,
    )


async def source_cmd(m: Message, _: I18nGettext):
    text = _(
        "Bot has open source code!\n\n"
        "Source: {link}"
    ).format(
        link=(
            "https://github.com/Desiders/get_anime_bot"
        )
    )

    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        selective=True,
        row_width=1,
        keyboard=[
            [KeyboardButton(text="/help")],
        ],
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        disable_notification=False,
        reply_markup=markup,
    )


async def language_cmd(
    m: Message,
    _: I18nGettext,
    dialog_manager: DialogManager,
):
    await dialog_manager.start(Language.main, mode=StartMode.RESET_STACK)


async def settings_cmd(
    m: Message,
    _: I18nGettext,
    dialog_manager: DialogManager,
):
    await dialog_manager.start(Settings.main, mode=StartMode.RESET_STACK)


def register_introduction_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_cmd,
        commands={"start", "help"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        genres_gif_cmd,
        commands={"genres_gif"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        genres_img_cmd,
        commands={"genres_img"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        genres_all_cmd,
        commands={"genres_all"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        source_cmd,
        commands={"source"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        language_cmd,
        commands={"language", "lang"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        settings_cmd,
        commands={"settings"},
        content_types={"text"},
        state="*",
    )
