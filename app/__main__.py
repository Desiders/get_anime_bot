import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config_reader import load_config
from .services.database import RedisDB
from .services.urls import GetUrl
from .utils.startup import startup

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    config = load_config()

    dp = Dispatcher(Bot(config.bot.token))
    dp['get_url'] = GetUrl()
    dp['database'] = RedisDB(
        host=config.database.host,
        port=config.database.port,
        db=config.database.db,
        password=config.database.password,
    )

    logger.info("Starting bot")
    try:
        await startup(dp)
        await dp.start_polling(
            allowed_updates=['message_handlers', 'callback_query_handlers'],
        )
    finally:
        await dp.bot.session.close()
        await dp['get_url'].close()
        await dp['database'].close()
        await dp['database'].wait_closed()


try:
    asyncio.run(main())
except (KeyboardInterrupt, SystemExit):
    logger.error("Bot stopped!")
