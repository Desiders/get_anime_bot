from app.infrastructure.database.models import ViewModel
from app.infrastructure.database.repositories.repo import Repo
from sqlalchemy import func, insert, select


class ViewsRepo(Repo):
    async def get_views_stats(self) -> int:
        result = await self.session.execute(
            select(func.count('*'))
            .select_from(ViewModel)
        )

        return result.scalar_one()

    async def get_views_stats_by_tg_id(self, tg_id: int) -> int:
        result = await self.session.execute(
            select(func.count('*'))
            .where(ViewModel.user_tg_id == tg_id)
            .group_by(ViewModel.user_tg_id)
        )

        return result.scalar_one()

    async def create(
        self,
        tg_id: int,
        media_id: int,
    ):
        await self.session.execute(
            insert(ViewModel)
            .values(
                user_tg_id=tg_id,
                media_id=media_id,
            )
        )
