from app.domain.media.dto.stats import Media, Stats
from app.infrastructure.database.models import MediaModel, ViewModel
from app.infrastructure.database.repositories.repo import Repo
from pydantic import parse_obj_as
from sqlalchemy import case, func, insert, select
from structlog import get_logger
from structlog.stdlib import BoundLogger

logger: BoundLogger = get_logger()


class MediaRepo(Repo):
    async def get_media_stats(self) -> Stats:
        query = select(
            func.count(1).label("total"),
            func.count(case([(MediaModel.media_type == "gif", 1)])).label("gif"),
            func.count(case([(MediaModel.media_type == "img", 1)])).label("img"),
            func.count(case([(MediaModel.media_type == "all", 1)])).label("all"),
            func.count(case([(MediaModel.is_sfw.is_(True), 1)])).label("sfw"),
            func.count(case([(MediaModel.is_sfw.is_(False), 1)])).label("nsfw"),
        )
        second_query = select(
            func.count(1).label("total"),
            MediaModel.genre.label("genre"),
            MediaModel.media_type.label("media_type"),
            MediaModel.is_sfw.label("is_sfw"),
        ).group_by(
            MediaModel.genre,
            MediaModel.media_type,
            MediaModel.is_sfw,
        )

        result = await self.session.execute(query)
        stats = result.one()

        result = await self.session.execute(second_query)
        media_stats = parse_obj_as(list[Media], result.all())

        return Stats(
            total=stats["total"],
            gif=stats["gif"],
            img=stats["img"],
            all=stats["all"],
            sfw=stats["sfw"],
            nsfw=stats["nsfw"],
            media=media_stats,
        )

    async def get_viewed_media_stats(self) -> Stats:
        query = (
            select(
                func.count(1).label("total"),
                func.count(case([(MediaModel.media_type == "gif", 1)])).label("gif"),
                func.count(case([(MediaModel.media_type == "img", 1)])).label("img"),
                func.count(case([(MediaModel.media_type == "all", 1)])).label("all"),
                func.count(case([(MediaModel.is_sfw.is_(True), 1)])).label("sfw"),
                func.count(case([(MediaModel.is_sfw.is_(False), 1)])).label("nsfw"),
            )
            .join(
                MediaModel,
                ViewModel.media_id == MediaModel.id,
            )
            .select_from(
                ViewModel,
            )
        )
        second_query = (
            select(
                func.count(1).label("total"),
                MediaModel.genre.label("genre"),
                MediaModel.media_type.label("media_type"),
                MediaModel.is_sfw.label("is_sfw"),
            )
            .join(
                MediaModel,
                ViewModel.media_id == MediaModel.id,
            )
            .select_from(
                ViewModel,
            )
            .group_by(
                MediaModel.genre,
                MediaModel.media_type,
                MediaModel.is_sfw,
            )
        )

        result = await self.session.execute(query)
        stats = result.one()

        result = await self.session.execute(second_query)
        media_stats = parse_obj_as(list[Media], result.all())

        return Stats(
            total=stats["total"],
            gif=stats["gif"],
            img=stats["img"],
            all=stats["all"],
            sfw=stats["sfw"],
            nsfw=stats["nsfw"],
            media=media_stats,
        )

    async def get_viewed_media_stats_by_tg_id(self, tg_id: int) -> Stats:
        query = (
            select(
                func.count(1).label("total"),
                func.count(case([(MediaModel.media_type == "gif", 1)])).label("gif"),
                func.count(case([(MediaModel.media_type == "img", 1)])).label("img"),
                func.count(case([(MediaModel.media_type == "all", 1)])).label("all"),
                func.count(case([(MediaModel.is_sfw.is_(True), 1)])).label("sfw"),
                func.count(case([(MediaModel.is_sfw.is_(False), 1)])).label("nsfw"),
            )
            .join(
                MediaModel,
                ViewModel.media_id == MediaModel.id,
            )
            .select_from(
                ViewModel,
            )
            .where(
                ViewModel.user_tg_id == tg_id,
            )
        )
        second_query = (
            select(
                func.count(1).label("total"),
                MediaModel.genre.label("genre"),
                MediaModel.media_type.label("media_type"),
                MediaModel.is_sfw.label("is_sfw"),
            )
            .join(
                MediaModel,
                ViewModel.media_id == MediaModel.id,
            )
            .select_from(
                ViewModel,
            )
            .group_by(
                MediaModel.genre,
                MediaModel.media_type,
                MediaModel.is_sfw,
            )
        )

        result = await self.session.execute(query)
        stats = result.one()

        result = await self.session.execute(second_query)
        media_stats = parse_obj_as(list[Media], result.all())

        return Stats(
            total=stats["total"],
            gif=stats["gif"],
            img=stats["img"],
            all=stats["all"],
            sfw=stats["sfw"],
            nsfw=stats["nsfw"],
            media=media_stats,
        )

    async def get_not_viewed(
        self,
        tg_id: int,
        genre: str,
        media_type: str,
        is_sfw: bool,
        limit: int = 1,
    ) -> list[MediaModel]:
        viewed_media_query = select(ViewModel.media_id).where(
            ViewModel.user_tg_id == tg_id,
        )
        query = (
            select(MediaModel)
            .where(
                MediaModel.genre == genre,
                MediaModel.media_type == media_type,
                MediaModel.is_sfw.is_(is_sfw),
                MediaModel.id.not_in(viewed_media_query),
            )
            .order_by(func.random())
            .limit(limit)
        )

        logger.info("Get not viewed media", query=str(query))

        result = await self.session.execute(query)

        return result.scalars().all()

    async def create(
        self,
        url: str,
        source_id: int,
        media_type: str,
        is_sfw: bool,
        genre: str | None = None,
    ):
        query = insert(MediaModel).values(
            url=url,
            genre=genre,
            source_id=source_id,
            media_type=media_type,
            is_sfw=is_sfw,
        )

        await self.session.execute(query)
