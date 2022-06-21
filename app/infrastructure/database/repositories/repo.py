from sqlalchemy.ext.asyncio import AsyncSession


class Repo:
    def __init__(self, session: AsyncSession):
        self.session = session
