from app.domain.media.dto.stats import Stats
from app.infrastructure.database.models import MediaModel, ViewModel
from app.infrastructure.database.repositories.repo import Repo
from sqlalchemy import case, func, insert, select


class MediaRepo(Repo):
    async def get_media_stats(self) -> Stats:
        query = select(
            func.count(MediaModel.id).label("total"),
            func.count(
                case([(MediaModel.media_type == "gif", 1)])).label("gif"),
            func.count(
                case([(MediaModel.media_type == "img", 1)])).label("img"),
            func.count(
                case([(MediaModel.media_type == "all", 1)])).label("all"),
            func.count(case([(MediaModel.is_sfw.is_(True), 1)])).label("sfw"),
            func.count(case([(MediaModel.is_sfw.is_(False), 1)])).label(
                "nsfw"),
        ).select_from(MediaModel)

        result = await self.session.execute(query)

        stats = result.one()

        return Stats.from_orm(stats)

    async def get_not_viewed(
        self,
        tg_id: int,
        genre: str,
        media_type: str,
        is_sfw: bool,
        limit: int = 1,
    ) -> list[MediaModel]:
        viewed_media = (
            select(ViewModel.media_id)
            .where(
                ViewModel.user_tg_id == tg_id,
            )
        )

        result = await self.session.execute(
            select(MediaModel)
            .where(
                MediaModel.genre == genre,
                MediaModel.media_type == media_type,
                MediaModel.is_sfw.is_(is_sfw),
                MediaModel.id.not_in(viewed_media),
            )
            .order_by(func.random())
            .limit(limit)
        )

        return result.scalars().all()

    async def create(
        self,
        url: str,
        source_id: int,
        media_type: str,
        is_sfw: bool,
        genre: str | None = None,
    ):
        await self.session.execute(
            insert(MediaModel)
            .values(
                url=url,
                genre=genre,
                source_id=source_id,
                media_type=media_type,
                is_sfw=is_sfw,
            )
        )
