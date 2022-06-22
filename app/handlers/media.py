from itertools import chain
from typing import Optional

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.exceptions import FileIsTooBig, WrongFileIdentifier
from aiohttp import ClientError
from app.filters import CheckGenreIn, NSFWSettings
from app.infrastructure.database.repositories import UnitOfWork
from app.infrastructure.media import Media, MediaSource
from app.typehints import I18nGettext
from sqlalchemy.exc import IntegrityError, NoResultFound
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


async def genre_cmd(
    m: Message,
    _: I18nGettext,
    sources: set[MediaSource],
    uow: UnitOfWork,
):
    genre = m.get_command(pure=True)

    media: Optional[Media] = None
    for source in sources:
        if genre in source.genres:
            try:
                media_many = await source.get_media(genre, count=1)
            except ClientError:
                logger.warning(
                    "Failed to get media",
                    exc_info=True,
                    stack_info=True,
                )
            else:
                media = media_many[0]
            break

    if media is None:
        await m.reply(
            text=_("No media found for this genre :("),
            parse_mode="HTML",
            disable_web_page_preview=True,
            disable_notification=False,
        )
        return

    try:
        if media.media_type == "gif":
            await m.reply_animation(
                media.url,
                parse_mode=None,
                disable_notification=False,
                allow_sending_without_reply=True,
            )
        else:
            await m.reply_document(
                media.url,
                parse_mode=None,
                disable_notification=False,
                allow_sending_without_reply=True,
            )
    except WrongFileIdentifier:
        logger.warning("Failed to send media", media=media)
        await genre_cmd(m, _, sources, uow)
        return
    except FileIsTooBig:
        logger.warning("Failed to send media. File is too big", media=media)
        await genre_cmd(m, _, sources, uow)

    source_name = source.__class__.__name__
    try:
        source_model = await uow.sources.get_by_name(source_name)
    except NoResultFound:
        # save the source to the database
        await uow.sources.create(source_name, source.SOURCE_URL)
        await uow.commit()

        source_model = await uow.sources.get_by_name(source_name)

    try:
        # save the media to the database
        await uow.media.create(
            url=media.url,
            source_id=source_model.id,
            media_type=media.media_type,
            is_sfw=media.is_sfw,
            genre=media.raw_genre,
        )
    except IntegrityError:
        pass
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
