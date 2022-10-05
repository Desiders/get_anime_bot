from app.infrastructure.database.models import MediaModel, ViewModel
from app.infrastructure.database.repositories.repo import Repo
from sqlalchemy import func, insert, select


class MediaRepo(Repo):
    async def get_count_media(self) -> int:
        result = await self.session.execute(
            select(func.count('*'))
            .select_from(MediaModel)
        )

        return result.scalar_one()

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
