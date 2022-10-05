from app.infrastructure.database.models import SourceModel
from app.infrastructure.database.repositories.repo import Repo
from sqlalchemy import func, insert, select


class SourceRepo(Repo):
    async def get_count_sources(self) -> int:
        result = await self.session.execute(
            select(func.count('*'))
            .select_from(SourceModel)
        )

        return result.scalar_one()

    async def get_by_name(self, name: str) -> SourceModel:
        result = await self.session.execute(
            select(SourceModel)
            .where(SourceModel.name == name)
        )

        return result.scalar_one()

    async def create(self, name: str, url: str):
        await self.session.execute(
            insert(SourceModel)
            .values(name=name, url=url)
        )
