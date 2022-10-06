from itertools import chain

from aiogram import Dispatcher
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.exceptions import FileIsTooBig, WrongFileIdentifier
from app.filters import CheckGenreIn, NSFWSettings
from app.infrastructure.database.repositories import UnitOfWork
from app.infrastructure.media import MediaSource
from app.infrastructure.media.base.schemas import MediaGenre
from app.typehints import I18nGettext
from sqlalchemy.exc import IntegrityError
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


async def genre_cmd(
    m: Message,
    _: I18nGettext,
    sources: set[MediaSource],
    uow: UnitOfWork,
):
    genre: str = m.get_command(pure=True)  # type: ignore

    media_genre: MediaGenre
    for source in sources:
        if genre not in source.genres:
            continue

        media_genre = source.parse_genre(genre)

    media_many = await uow.media.get_not_viewed(
        tg_id=m.from_user.id,
        genre=media_genre.raw_genre,
        media_type=media_genre.media_type,
        is_sfw=media_genre.is_sfw,
        limit=5,
    )

    if not media_many:
        await m.reply(
            text=_(
                "Not viewed media not found for this genre to you :(\n"
                "Try again later, please!",
            ),
            parse_mode="HTML",
            disable_web_page_preview=True,
            disable_notification=False,
        )
        return
    else:
        media = media_many[0]

    if m.chat.type == "private":
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=False,
            row_width=1,
            keyboard=[
                [KeyboardButton(text=f"/{genre}")],
                [KeyboardButton(text="/help")],
            ],
        )
    else:
        markup = None

    try:
        if media.media_type == "gif":
            await m.reply_animation(
                media.url,
                parse_mode=None,
                disable_notification=False,
                allow_sending_without_reply=True,
                reply_markup=markup,
            )
        else:
            await m.reply_document(
                media.url,
                parse_mode=None,
                disable_notification=False,
                allow_sending_without_reply=True,
                reply_markup=markup,
            )
    except WrongFileIdentifier:
        logger.warning("Failed to send media", media=media)

        await genre_cmd(m, _, sources, uow)
        return
    except FileIsTooBig:
        logger.warning("Failed to send media. File is too big", media=media)

        await genre_cmd(m, _, sources, uow)

    try:
        await uow.views.create(
            tg_id=m.from_user.id,
            media_id=media.id,
        )
    except IntegrityError:
        await uow.rollback()
    else:
        await uow.commit()


async def forbidden_genre_cmd_private(m: Message, _: I18nGettext):
    await m.answer(
        text=_(
            "You aren't allowed to see nsfw content!\n\n"
            "/settings — change settings"
        ),
        parse_mode="HTML",
        disable_web_page_preview=True,
        disable_notification=False,
    )


async def forbidden_genre_cmd_public(m: Message, _: I18nGettext):
    await m.answer(
        text=_(
            "You can't see nsfw content not in private messages! ^_^"
        ),
        parse_mode="HTML",
        disable_web_page_preview=True,
        disable_notification=False,
    )


def register_genre_handlers(dp: Dispatcher, *sources: MediaSource):
    sfw_genres = chain.from_iterable(
        source.sfw_genres for source in sources
    )
    nsfw_genres = chain.from_iterable(
        source.nsfw_genres for source in sources
    )

    SFWGenres = CheckGenreIn(genres=sfw_genres)
    NSFWGenres = CheckGenreIn(genres=nsfw_genres)

    dp.register_message_handler(
        genre_cmd,
        SFWGenres,
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        genre_cmd,
        NSFWGenres,
        NSFWSettings(can_show_nsfw=True),
        content_types={"text"},
        chat_type="private",
        state="*",
    )
    dp.register_message_handler(
        forbidden_genre_cmd_private,
        NSFWGenres,
        NSFWSettings(can_show_nsfw=False),
        content_types={"text"},
        chat_type="private",
        state="*",
    )
    dp.register_message_handler(
        forbidden_genre_cmd_public,
        NSFWGenres,
        content_types={"text"},
        state="*",
    )
