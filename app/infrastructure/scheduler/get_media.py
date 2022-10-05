import asyncio
from itertools import cycle
from typing import NoReturn

from aiohttp import ClientError
from app.infrastructure.database.repositories import UnitOfWork
from app.infrastructure.media import (MediaSource, NekosFun, NekosLife,
                                      WaifuPics)
from app.infrastructure.media.base.schemas import Media
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import sessionmaker
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()

SLEEP_FOR_NEKOS_FUN = 0.5
SLEEP_FOR_NEKOS_LIFE = 0.3
SLEEP_FOR_WAIFU_PICS = 0.3

SLEEP_AFTER_ERROR = 5


async def create_source_and_get_source_id(
    source: MediaSource,
    uow: UnitOfWork,
) -> int:
    source_name = source.__class__.__name__
    try:
        source_model = await uow.sources.get_by_name(source_name)
    except NoResultFound:
        # save the source to the database
        await uow.sources.create(source_name, source.SOURCE_URL)
        await uow.commit()

        source_model = await uow.sources.get_by_name(source_name)

    return source_model.id  # type: ignore


async def create_media(
    media: Media,
    source_id: int,
    uow: UnitOfWork,
):
    await uow.media.create(
        url=media.url,
        source_id=source_id,
        media_type=media.media_type,
        is_sfw=media.is_sfw,
        genre=media.raw_genre,
    )


async def parse_nekos_fun(
    source: NekosFun,
    uow: UnitOfWork,
) -> NoReturn:  # type: ignore
    source_id = await create_source_and_get_source_id(source, uow)

    for genre in cycle(source.genres):
        try:
            media_many = await source.get_media(genre, count=5)
        except ClientError:
            logger.warning(
                "Failed to get media",
                exc_info=True,
                stack_info=True,
            )
            await asyncio.sleep(SLEEP_AFTER_ERROR)
            continue

        for media in media_many:
            try:
                await create_media(media, source_id, uow)
            except IntegrityError:
                await uow.rollback()
            else:
                await uow.commit()
        await asyncio.sleep(SLEEP_FOR_NEKOS_FUN)


async def parse_nekos_life(
    source: NekosLife,
    uow: UnitOfWork,
) -> NoReturn:  # type: ignore
    source_id = await create_source_and_get_source_id(source, uow)

    for genre in cycle(source.genres):
        try:
            media_many = await source.get_media(genre, count=20)
        except ClientError:
            logger.warning(
                "Failed to get media",
                exc_info=True,
                stack_info=True,
            )
            await asyncio.sleep(SLEEP_AFTER_ERROR)
            continue

        for media in media_many:
            try:
                await create_media(media, source_id, uow)
            except IntegrityError:
                await uow.rollback()
            else:
                await uow.commit()
        await asyncio.sleep(SLEEP_FOR_NEKOS_LIFE)


async def parse_waifu_pics(
    source: WaifuPics,
    uow: UnitOfWork,
) -> NoReturn:  # type: ignore
    source_id = await create_source_and_get_source_id(source, uow)

    for genre in cycle(source.genres):
        try:
            media_many = await source.get_media(genre, count=30)
        except ClientError:
            logger.warning(
                "Failed to get media",
                exc_info=True,
                stack_info=True,
            )
            await asyncio.sleep(SLEEP_AFTER_ERROR)
            continue

        for media in media_many:
            try:
                await create_media(media, source_id, uow)
            except IntegrityError:
                await uow.rollback()
            else:
                await uow.commit()

        await asyncio.sleep(SLEEP_FOR_WAIFU_PICS)


async def create_uow(
    sa_sessionmaker: sessionmaker,
) -> UnitOfWork:
    async with sa_sessionmaker() as session:
        return UnitOfWork(session)


async def start_parse_media(
    sources: set[MediaSource],
    sa_sessionmaker: sessionmaker,
):
    tasks = []
    for source in sources:
        if isinstance(source, NekosFun):
            tasks.append(
                parse_nekos_fun(
                    source,
                    await create_uow(sa_sessionmaker),
                ),
            )
        elif isinstance(source, NekosLife):
            tasks.append(
                parse_nekos_life(
                    source,
                    await create_uow(sa_sessionmaker),
                ),
            )
        elif isinstance(source, WaifuPics):
            tasks.append(
                parse_waifu_pics(
                    source,
                    await create_uow(sa_sessionmaker),
                ),
            )
        else:
            raise NotImplementedError("Unknown source")

    asyncio.gather(*tasks, return_exceptions=False)
