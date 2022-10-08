from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.text_decorations import html_decoration as html_dec
from aiogram_dialog import DialogManager, StartMode
from app.states import Language, MainMenu, Settings, Stats
from app.typehints import I18nGettext


async def menu_cmd(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        MainMenu.main_menu,
        data={"user": m.from_user},
        mode=StartMode.RESET_STACK,
    )


async def source_cmd(m: Message, _: I18nGettext):
    text = _(
        "The bot has open source code!\n\n"
        "{source_link}"
    ).format(
        source_link=html_dec.link(
            "Source code",
            "https://github.com/Desiders/get_anime_bot",
        ),
    )

    await m.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )


async def language_cmd(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        Language.select_language,
        mode=StartMode.RESET_STACK,
    )


async def settings_cmd(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        Settings.select_settings,
        mode=StartMode.RESET_STACK,
    )


async def stats_cmd(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        Stats.select_stats_type,
        mode=StartMode.RESET_STACK,
    )


def register_introduction_handlers(dp: Dispatcher):
    dp.register_message_handler(
        menu_cmd,
        commands={"start", "help", "menu"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        source_cmd,
        commands={"source"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        language_cmd,
        commands={"language", "lang"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        settings_cmd,
        commands={"settings"},
        content_types={"text"},
        state="*",
    )
    dp.register_message_handler(
        stats_cmd,
        commands={"statistics", "stats"},
        content_types={"text"},
        state="*",
    )
