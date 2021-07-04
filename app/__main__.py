import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher

from .services import GetUrl
from .utils import shutdown, startup

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    dispatcher = Dispatcher(Bot(token=getenv("BOT_TOKEN")))
    dispatcher['get_url'] = GetUrl()

    logger.info("Starting bot")
    try:
        await startup(dispatcher)
        await dispatcher.start_polling(allowed_updates=['message_handlers'])
    finally:
        await shutdown(dispatcher)


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logger.error("Bot stopped!")
