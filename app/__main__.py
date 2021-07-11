import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config_reader import load_config
from .services.database import RedisDB
from .services.urls import GetUrl
from .utils.startup import startup

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    config = load_config()

    dispatcher = Dispatcher(Bot(token=config.bot.token))
    dispatcher['get_url'] = GetUrl()
    dispatcher['database'] = RedisDB(host=config.database.host,
                                     port=config.database.port,
                                     db=config.database.db,
                                     password=config.database.password)

    logger.info("Starting bot")
    try:
        await startup(dispatcher)
        await dispatcher.start_polling(allowed_updates=['message_handlers'])
    finally:
        await dispatcher.bot.session.close()
        await dispatcher['get_url'].close()
        await dispatcher['database'].close()
        await dispatcher['database'].wait_closed()


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logger.error("Bot stopped!")
