import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.types import BotCommand

from .handlers import register_handlers
from .services import GetUrl

logger = logging.getLogger(__name__)

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Get menu!"),
    ]
    commands.extend([
        BotCommand(command=command, description=f"Get {command}!")
            for command in GetUrl.urls
    ])
    await bot.set_my_commands(commands)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    get_url = GetUrl()
    bot = Bot(token=getenv("BOT_TOKEN"))

    await set_bot_commands(bot)

    dispatcher = Dispatcher(bot)
    dispatcher.setup_middleware(EnvironmentMiddleware(dict(get_url=get_url)))

    register_handlers(dispatcher)

    logger.info("Starting bot")

    try:
        await dispatcher.start_polling(allowed_updates=["message_handlers"])
    finally:
        await dispatcher.bot.session.close()
        await get_url.close()

try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logger.error("Bot stopped!")
