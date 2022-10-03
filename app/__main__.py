import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.types import (BotCommand, BotCommandScopeAllGroupChats,
                           BotCommandScopeAllPrivateChats)
from aiogram_dialog import DialogRegistry
from structlog import get_logger
from structlog.stdlib import BoundLogger

from app.config_reader import load_config
from app.constants import LOCALES_DIR
from app.dialogs import language_dialog, settings_dialog
from app.handlers import (register_error_handlers, register_genre_handlers,
                          register_introduction_handlers)
from app.infrastructure.database import make_connection_string, sa_sessionmaker
from app.infrastructure.media import NekosFun, NekosLife, WaifuPics
from app.language_utils.language import DEFAULT_LANGUAGE
from app.logging_config import logging_configure
from app.middlewares import ACLMiddleware, DatabaseMiddleware, I18nMiddleware

logger: BoundLogger = get_logger()


async def set_bot_commands(bot: Bot):
    cmd_help = BotCommand(
        command="help",
        description="Show menu",
    )
    cmd_gif = BotCommand(
        command="genres_gif",
        description="GIF by genre",
    )
    cmd_img = BotCommand(
        command="genres_img",
        description="image by genre",
    )
    cmd_all = BotCommand(
        command="genres_all",
        description=" GIF or image by genre",
    )
    cmd_source = BotCommand(
        command="source",
        description="Show source code",
    )

    public = [
        cmd_help, cmd_gif,
        cmd_img, cmd_all,
    ]
    private = [
        cmd_help, cmd_gif,
        cmd_img, cmd_all,
        cmd_source,
    ]

    await bot.set_my_commands(public, BotCommandScopeAllGroupChats())
    await bot.set_my_commands(private, BotCommandScopeAllPrivateChats())


async def main():
    logging_configure()
    logger.info("Logging is configured")

    config = load_config()
    logger.info("Configuration loaded")

    bot = Bot(
        token=config.bot.token,
        parse_mode=None,
        disable_web_page_preview=None,
    )
    dp = Dispatcher(
        bot=bot,
        storage=MemoryStorage(),
    )

    nekos_life = NekosLife()
    nekos_fun = NekosFun()
    waifu_pics = WaifuPics()

    await set_bot_commands(bot)
    logger.info("Bot commands are set")

    dp.setup_middleware(DatabaseMiddleware(
        sa_sessionmaker(make_connection_string(config.database)),
    ))
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(I18nMiddleware(
        domain="bot",
        path=LOCALES_DIR,
        default=DEFAULT_LANGUAGE.code,
    ))
    dp.setup_middleware(EnvironmentMiddleware({
        "sources": {nekos_life, nekos_fun, waifu_pics},
    }))
    logger.info("Middlewares are registered")

    register_introduction_handlers(dp)
    register_genre_handlers(dp, nekos_life, nekos_fun, waifu_pics)
    register_error_handlers(dp)
    logger.info("Handlers are registered")

    registry = DialogRegistry(dp)
    registry.register(language_dialog)
    registry.register(settings_dialog)
    logger.info("Dialogs are registered")

    try:
        logger.info("Bot starting!")
        await dp.start_polling(
            allowed_updates=[
                "message_handlers", "callback_query_handlers",
            ],
        )
    finally:
        logger.error("Bot stopped!")

        bot_session = await bot.get_session()
        if bot_session is not None:
            await bot_session.close()
        logger.warning("Bot session closed")

        await nekos_life.close()
        await nekos_fun.close()
        await waifu_pics.close()
        logger.warning("Closed sources")


asyncio.run(main())
