from app.infrastructure.database.models import MediaModel, ViewModel
from app.infrastructure.database.repositories.repo import Repo
from sqlalchemy import and_, func, insert, select


class MediaRepo(Repo):
    async def get_count_media(self) -> int:
        result = await self.session.execute(
            select(func.count('*'))
            .select_from(MediaModel)
        )

        return result.scalar_one()

    async def get_by_url(self, url: str) -> MediaModel:
        result = await self.session.execute(
            select(MediaModel)
            .where(MediaModel.url == url)
        )

        return result.scalar_one()

    async def get_not_viewed(
        self,
        tg_id: int,
        limit: int = 1,
    ) -> list[MediaModel]:
        viewed_media = (
            select(ViewModel.media_id)
            .where(
                ViewModel.user_tg_id == tg_id
            )
        )

        result = await self.session.execute(
            select(MediaModel)
            .where(
                MediaModel.id.not_in(viewed_media)
            )
            .limit(limit)
        )

        return result.scalars().all()

    async def get_not_viewed_with_age_limit(
        self,
        tg_id: int,
        is_sfw: bool = True,
        limit: int = 1,
    ) -> list[MediaModel]:
        viewed_media = (
            select(ViewModel.media_id)
            .where(
                ViewModel.user_tg_id == tg_id
            )
        )

        result = await self.session.execute(
            select(MediaModel)
            .where(
                and_(
                    MediaModel.is_sfw == is_sfw,
                    MediaModel.id.not_in(viewed_media)
                )
            )
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
                url=url, genre=genre, source_id=source_id,
                media_type=media_type, is_sfw=is_sfw,
            )
        )
