from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from app.infrastructure.database.repositories import UnitOfWork
from sqlalchemy.exc import NoResultFound


class ACLMiddleware(BaseMiddleware):
    async def on_pre_process_message(
        self,
        message: Message,
        data: dict,
    ):
        await self.create_user(message, data)

    async def on_pre_process_callback_query(
        self,
        query: CallbackQuery,
        data: dict,
    ):
        await self.create_user(query, data)

    async def create_user(
        self,
        obj: CallbackQuery | Message,
        data: dict,
    ):
        uow: UnitOfWork = data["uow"]

        tg_id = obj.from_user.id

        try:
            user = await uow.users.get_by_tg_id(tg_id)
        except NoResultFound:
            await uow.users.create(tg_id)
            await uow.commit()

            user = await uow.users.get_by_tg_id(tg_id)

        data["user"] = user
        obj.bot["user"] = user
