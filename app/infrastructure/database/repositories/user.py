from typing import Optional

from app.infrastructure.database.models import UserModel
from app.infrastructure.database.repositories.repo import Repo
from sqlalchemy import insert, select, update


class UserRepo(Repo):
    async def get_by_tg_id(self, tg_id: int) -> UserModel:
        result = await self.session.execute(
            select(UserModel)
            .where(UserModel.tg_id == tg_id)
        )

        return result.scalar_one()

    async def create(
        self,
        tg_id: int,
        language_code: Optional[str] = None,
    ):
        await self.session.execute(
            insert(UserModel)
            .values(tg_id=tg_id, language_code=language_code)
        )

    async def update_language_code(
        self,
        tg_id: int,
        language_code: str,
    ):
        await self.session.execute(
            update(UserModel)
            .where(UserModel.tg_id == tg_id)
            .values(language_code=language_code)
        )

    async def update_show_nsfw(
        self,
        tg_id: int,
        show_nsfw: bool,
    ):
        await self.session.execute(
            update(UserModel)
            .where(UserModel.tg_id == tg_id)
            .values(show_nsfw=show_nsfw)
        )
