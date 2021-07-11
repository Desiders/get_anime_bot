from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.types import BotCommand

from ..handlers import register_handlers
from ..services.urls import GetUrl


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Get menu!"),
    ]
    commands.extend([
        BotCommand(command=genre, description=f"Get {genre}!")
            for genre in GetUrl.genres
    ])
    await bot.set_my_commands(commands)


async def startup(dispatcher: Dispatcher) -> None:
    await set_bot_commands(dispatcher.bot)

    register_handlers(dispatcher)

    dispatcher.setup_middleware(
        EnvironmentMiddleware(
            dict(
                get_url=dispatcher['get_url'],
                database=dispatcher['database']
            )
        )
    )
