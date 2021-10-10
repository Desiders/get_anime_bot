from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware

from ..handlers import register_handlers
from ..services.urls import GetUrl


async def set_bot_commands(bot: Bot):
    commands = [
        types.BotCommand(
            command="start",
            description="Get menu!",
        )
    ]
    commands.extend([
        types.BotCommand(
            command=genre,
            description=f"Get {genre}!",
        )
        for genre in GetUrl.sfw_genres
    ])

    await bot.set_my_commands(commands)


async def startup(dp: Dispatcher):
    await set_bot_commands(dp.bot)

    dp.setup_middleware(
        EnvironmentMiddleware({
            "get_url": dp['get_url'],
            "database": dp['database'],
        })
    )

    register_handlers(dp)
