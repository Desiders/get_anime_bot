from aiogram import Dispatcher

from ..services import GetUrl


async def shutdown(dispatcher: Dispatcher) -> None:
    get_url: GetUrl = dispatcher['get_url']

    await dispatcher.bot.session.close()
    await get_url.close()
