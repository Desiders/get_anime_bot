import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.types import (BotCommand, BotCommandScopeAllGroupChats,
                           BotCommandScopeAllPrivateChats)
from aiogram_dialog import DialogRegistry
from sqlalchemy.orm import sessionmaker
from structlog import get_logger
from structlog.stdlib import BoundLogger

from app.config_reader import load_config
from app.constants import LOCALES_DIR
from app.dialogs import (language_dialog, main_menu_dialog, settings_dialog,
                         stats_dialog)
from app.handlers import (register_error_handlers, register_genre_handlers,
                          register_introduction_handlers)
from app.infrastructure.database import make_connection_string, sa_sessionmaker
from app.infrastructure.media import (MediaSource, NekosFun, NekosLife,
                                      WaifuPics)
from app.infrastructure.scheduler import start_parse_media
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
    cmd_language = BotCommand(
        command="language",
        description="Change language",
    )
    cmd_settings = BotCommand(
        command="settings",
        description="Change settings",
    )
    cmd_stats = BotCommand(
        command="stats",
        description="Show statistics",
    )

    public = [
        cmd_help, cmd_gif,
        cmd_img, cmd_all,
    ]
    private = [
        cmd_help, cmd_gif,
        cmd_img, cmd_all,
        cmd_source, cmd_language,
        cmd_settings, cmd_stats,
    ]

    await bot.set_my_commands(public, BotCommandScopeAllGroupChats())
    await bot.set_my_commands(private, BotCommandScopeAllPrivateChats())


async def start_scheduler(
    sources: set[MediaSource],
    sa_sessionmaker: sessionmaker,
):
    await start_parse_media(sources, sa_sessionmaker)


def setup_middlewares(
    dp: Dispatcher,
    sources: set[MediaSource],
    sm: sessionmaker,
):
    dp.setup_middleware(DatabaseMiddleware(sm))
    dp.setup_middleware(ACLMiddleware())
    dp.setup_middleware(I18nMiddleware(
        domain="bot",
        path=LOCALES_DIR,
        default=DEFAULT_LANGUAGE.code,
    ))
    dp.setup_middleware(EnvironmentMiddleware({"sources": sources}))


def register_handlers(dp: Dispatcher, sources: set[MediaSource]):
    register_introduction_handlers(dp)
    register_genre_handlers(dp, sources)
    register_error_handlers(dp)
    logger.info("Handlers are registered")


def register_dialogs(dr: DialogRegistry):
    dr.register(main_menu_dialog)
    dr.register(language_dialog)
    dr.register(settings_dialog)
    dr.register(stats_dialog)
    logger.info("Dialogs are registered")


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
    dr = DialogRegistry(dp)

    nekos_life = NekosLife()
    nekos_fun = NekosFun()
    waifu_pics = WaifuPics()

    sources: set[MediaSource] = {nekos_life, nekos_fun, waifu_pics}

    sm = sa_sessionmaker(make_connection_string(config.database))

    await set_bot_commands(bot)
    logger.info("Bot commands are set")

    setup_middlewares(dp, sources, sm)
    logger.info("Middlewares are registered")

    register_handlers(dp, sources)
    logger.info("Handlers are registered")

    register_dialogs(dr)
    logger.info("Dialogs are registered")

    await start_scheduler(sources, sm)
    logger.info("Scheduler is started")

    try:
        logger.info("Bot starting!")
        await dp.start_polling(
            allowed_updates=[
                "message_handlers",
                "callback_query_handlers",
            ],
        )
    finally:
        logger.error("Bot stopped!")

        for source in sources:
            await source.close()
        logger.warning("Closed sources")


asyncio.run(main())
