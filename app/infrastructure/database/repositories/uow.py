from typing import Optional

from app.infrastructure.database.repositories.media import MediaRepo
from app.infrastructure.database.repositories.source import SourceRepo
from app.infrastructure.database.repositories.user import UserRepo
from app.infrastructure.database.repositories.views import ViewsRepo
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

        self._media_repo: Optional[MediaRepo] = None
        self._source_repo: Optional[SourceRepo] = None
        self._user_repo: Optional[UserRepo] = None
        self._views_repo: Optional[ViewsRepo] = None

    @property
    def media(self):
        if self._media_repo is None:
            self._media_repo = MediaRepo(self.session)
        return self._media_repo

    @property
    def sources(self):
        if self._source_repo is None:
            self._source_repo = SourceRepo(self.session)
        return self._source_repo

    @property
    def users(self):
        if self._user_repo is None:
            self._user_repo = UserRepo(self.session)
        return self._user_repo

    @property
    def views(self):
        if self._views_repo is None:
            self._views_repo = ViewsRepo(self.session)
        return self._views_repo

    async def commit(self):
        await self.session.commit()

    async def close(self):
        await self.session.close()
