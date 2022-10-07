from itertools import chain

from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.text_decorations import html_decoration as html_dec
from aiogram_dialog import DialogManager, StartMode
from app.infrastructure.database.models import UserModel
from app.infrastructure.media import MediaSource
from app.states import Language, Settings, Stats
from app.typehints import I18nGettext


async def start_cmd(m: Message, _: I18nGettext):
    text = _(
        "Hi, {first_name}!\n\n"
        "Get an anime GIF or image by genre!\n"
        "/genres_gif\n"
        "/genres_img\n"
        "/genres_all\n\n"
        "/language — change the language\n"
        "/settings — change the settings\n"
        "/stats — view the statistics"
    ).format(
        first_name=m.from_user.first_name,
    )

    await m.answer(text, reply_markup=ReplyKeyboardRemove())


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
        "Genres:\n\n{genres}"
    ).format(
        genres=" ".join(map(lambda string: "/" + string, genres)),
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
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
        "Genres:\n\n{genres}"
    ).format(
        genres=" ".join(map(lambda string: "/" + string, genres)),
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
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
        "Genres:\n\n{genres}"
    ).format(
        genres=" ".join(map(lambda string: "/" + string, genres)),
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )


async def source_cmd(m: Message, _: I18nGettext):
    text = _(
        "The bot is open source!\n\n"
        "{source_link}"
    ).format(
        source_link=html_dec.link(
            "Source code",
            "https://github.com/Desiders/get_anime_bot",
        ),
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )


async def language_cmd(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        Language.select_language,
        mode=StartMode.RESET_STACK,
    )


async def settings_cmd(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        Settings.select_settings,
        mode=StartMode.RESET_STACK,
    )


async def stats_cmd(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        Stats.select_stats_type,
        mode=StartMode.RESET_STACK,
    )


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
    dp.register_message_handler(
        stats_cmd,
        commands={"statistics", "stats"},
        content_types={"text"},
        state="*",
    )
