from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, Message
from app.infrastructure.database.repositories import UnitOfWork
from sqlalchemy.orm import sessionmaker


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = {"update"}

    def __init__(self, sa_sessionmaker: sessionmaker):
        self.sa_sessionmaker = sa_sessionmaker

        super().__init__()

    async def pre_process(self, message: Message, data: dict, *args):
        await self.setup_uow(message, data)

    async def setup_uow(
        self,
        obj: Message | CallbackQuery,
        data: dict,
    ):
        async with self.sa_sessionmaker() as session:
            uow = UnitOfWork(session=session)

            data["uow"] = uow
            obj.bot["uow"] = uow

    async def post_process(self, query, data: dict, *args):
        await self.clear_uow(data)

    async def clear_uow(self, data: dict):
        uow: UnitOfWork = data["uow"]

        await uow.close()

        del data["uow"]
