from app.infrastructure.database.models import ViewModel
from app.infrastructure.database.repositories.repo import Repo
from sqlalchemy import insert


class ViewsRepo(Repo):
    async def create(
        self,
        tg_id: int,
        media_id: int,
    ):
        query = insert(ViewModel).values(user_tg_id=tg_id, media_id=media_id)

        await self.session.execute(query)
